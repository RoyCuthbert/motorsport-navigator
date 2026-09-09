from django.contrib import admin

from .models import (CoDriverProfile, CoDriverEmergencyContact,)
# Register your models here.
@admin.register(CoDriverProfile)
class CoDriverProfileAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "motorsport_uk_number",
        "club_membership_number",
        "created_on",
    )

    search_fields = (
        "first_name",
        "last_name",
        "motorsport_uk_number",
        "club_membership_number",
        "user__username",
        "user__email",
    )

@admin.register(CoDriverEmergencyContact)
class CoDriverEmergencyContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "relationship",
        "phone",
        "profile",
    )

    search_fields = (
        "name",
        "relationship",
        "phone",
        "profile__first_name",
        "profile__last_name",
    )