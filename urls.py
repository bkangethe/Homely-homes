from django.urls import path
from .views import (
    IssueCreate,
    IssuesList,
    create_house,
    create_tenant,
    dash,
    house_view,
    house_rent_records,
    login_view,
    logout_view,
    register,
    rent_records,
    tenants,
    delete_house,
    delete_issue,
    delete_rent_record,
    delete_tenant,
)


# urls to access different pages
urlpatterns = [
    path("", dash, name="dash"),
    path("house/create", create_house, name="create_house"),
    path("house/delete/<int:house_id>", delete_house, name="delete_house"),
    path("tenant/create", create_tenant, name="create_tenant"),
    path("tenant/delete/<int:tenant_id>", delete_tenant, name="delete_tenant"),
    path("house/<int:house_id>", house_view, name="house"),
    path("house/<int:house_id>/rent_records", house_rent_records, name="rent_records"),
    path("tenants", tenants, name="tenants"),
    path("rent_records", rent_records, name="rent_records"),
    path("rent_record/delete/<int:record_id>", delete_rent_record, name="delete_rent_records"),
    path("register", register, name="register"),
    path("login", login_view, name="login"),
    path("issue/create", IssueCreate.as_view(), name="issue_create"),
    path("issue", IssuesList.as_view(), name="issues"),
    path("issue/delete/<int:issue_id>", delete_issue, name="delete_issue"),
    path("logout", logout_view, name="logout"),
]
