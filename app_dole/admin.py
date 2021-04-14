from django.contrib import admin

# Register your models here.
from .models import (
    Barangay,
    Sms_Config,
    Sms_Bluster,
)
admin.site.register(Barangay)
admin.site.register(Sms_Bluster)
admin.site.register(Sms_Config)
