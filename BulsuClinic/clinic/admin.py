from django.contrib import admin
from .models import CustomUser, Staff, Patient

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
