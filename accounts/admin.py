from django.contrib import admin

from .models import DriverProfile
from .models import EmergencyContact

# Register your models here.

admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "motorsport_licence",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "relationship",
        "phone",
    )