from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView
from main.utils import get_balance
from .forms import CreateHouse, CreateRentRecord, CreateTenant, SignUpForm
from .models import House, Issue, RentRecord, Tenant
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


# Register a user
def register(request):
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = SignUpForm()
        return redirect("login")

    context = {"form": form}

    return render(request, "registration/register.html", context)


# log in users
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "Login successfull")
            return redirect("/dash")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "registration/login.html")


# logout users
def logout_view(requst):
    logout(requst)
    return redirect("login")


# generic class view to create issues
class IssueCreate(CreateView):
    model = Issue
    fields = ["house", "problem", "description"]
    template_name = "issue_create.html"
    success_url = "/dash/issue"


# generic class view to list issues
class IssuesList(ListView):
    model = Issue
    fields = ["house", "problem", "description", "date"]
    template_name = "issues.html"
    context_object_name = "issues"


# this is a view to render the dashboard. user login is required to access this page
@login_required
def dash(request):
    houses = House.objects.all()

    context = {"houses": houses}

    return render(request, "dash.html", context)


# function view to create a house
def create_house(request):
    create_house_form = CreateHouse(request.POST or None)

    if create_house_form.is_valid():
        create_house_form.save()
        create_house_form = CreateHouse()

    context = {"create_house_form": create_house_form}

    return render(request, "create_house.html", context)


# function view to create a tenant record
def create_tenant(request):
    create_tenant_form = CreateTenant(request.POST or None)

    if create_tenant_form.is_valid():
        create_tenant_form.save()
        create_tenant_form = CreateTenant()

    context = {"create_tenant_form": create_tenant_form}

    return render(request, "create_tenant.html", context)


# function view to render tenants list
def tenants(request):
    tenants = Tenant.objects.all()
    context = {"tenants": tenants}

    return render(request, "tenants.html", context)


# View to dispay house details
# Also has a provision to edit house information and create tenant records
def house_view(request, house_id):
    house = House.objects.get(id=house_id)
    edit_house_form = CreateHouse(instance=house)
    create_rent_record_form = CreateRentRecord()
    rent_records = RentRecord.objects.filter(house=house)

    if request.method == "POST":
        edit_house_form = CreateHouse(request.POST)
        if edit_house_form.is_valid():
            edit_house_form.save()
            # send a message to client side to show success or failure.
            messages.add_message(
                request, messages.SUCCESS, "House created successfully."
            )
        else:
            messages.add_message(request, messages.ERROR, "House creation failed.")

    context = {
        "house": house,
        "edit_house_form": edit_house_form,
        "create_rent_record_form": create_rent_record_form,
        "rent_records": rent_records,
    }
    return render(request, "house.html", context)


def delete_rent_record(request, record_id):
    queryset = RentRecord.objects.filter(id=record_id)
    house_id = None
    if queryset.exists():
        record = queryset.first()
        house_id = record.house.id
        record.delete()
        messages.add_message(request, messages.SUCCESS, "Rent record deleted")
    else:
        messages.add_message(request, messages.ERROR, "Rent record does not exist")

    return redirect(house_view, house_id=house_id)


def delete_tenant(request, tenant_id):
    queryset = Tenant.objects.filter(id=tenant_id)
    if queryset.exists():
        tenant = queryset.first()
        tenant.delete()
        messages.add_message(request, messages.SUCCESS, "Tenant record deleted")
    else:
        messages.add_message(request, messages.ERROR, "Tenant record does not exist")
    return redirect("tenants")


def delete_house(request, house_id):
    queryset = House.objects.filter(id=house_id)
    if queryset.exists():
        house = queryset.first()
        house.delete()
        messages.add_message(cathrequest, messages.SUCCESS, "House record deleted")
    else:
        messages.add_message(request, messages.ERROR, "House record does not exist")
    return redirect("dash")


def delete_issue(request, issue_id):
    queryset = Issue.objects.filter(id=issue_id)
    if queryset.exists():
        issue = queryset.first()
        issue.delete()
        messages.add_message(request, messages.SUCCESS, "Issue deleted")
    else:
        messages.add_message(request, messages.ERROR, "Issue does not exist")
    return redirect("issues")


# Function view to list all rent records
def rent_records(request):
    rent_records = RentRecord.objects.all()

    context = {"rent_records": rent_records}

    return render(request, "rent_records.html", context)


# Function view to list house rent records
def house_rent_records(request, house_id):
    house = House.objects.get(id=house_id)
    rent_records = RentRecord.objects.filter(house=house)
    # A post request can be sent to this view to create a rent record
    if request.method == "POST":
        create_rent_record_form = CreateRentRecord(request.POST)
        if create_rent_record_form.is_valid():
            obj = create_rent_record_form.save(commit=False)
            amount_paid = create_rent_record_form.cleaned_data["amount_paid"]

            # use a utility function to calculate balance based on previous records
            balance = get_balance(house.id, amount_paid)
            obj.house = house
            obj.balance = balance
            obj.save()
            messages.add_message(
                request, messages.SUCCESS, "Record created successfully"
            )
            return redirect(house_view, house_id=house.id)
        else:
            messages.add_message(request, messages.ERROR, "Record creation failed")
            return redirect(house_view, house_id=house.id)

    context = {"rent_records": rent_records}

    return render(request, "rent_records.html", context)
