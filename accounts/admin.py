from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import DriverProfile, EmergencyContact


# Register your models here.

admin.register(DriverProfile)
class DriverProfileAdmin(ModelAdmin):

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
class EmergencyContactAdmin(ModelAdmin):

    list_display = (
        "name",
        "relationship",
        "phone",
    )