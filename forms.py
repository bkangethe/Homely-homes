from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import House, RentRecord, Tenant

class CreateHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = ['number', 'tenant', 'rent']


class CreateTenant(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'email', 'phone_number']

class CreateRentRecord(forms.ModelForm):
    class Meta:
        model = RentRecord
        fields = ['amount_paid', 'confirmation_code']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')