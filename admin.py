from django.contrib import admin
from .models import House, Tenant, RentRecord, Issue

# Register your models here.
admin.site.register(House)
admin.site.register(Tenant)
admin.site.register(RentRecord)
admin.site.register(Issue)
