from django.contrib import admin
from .models import Vehicle, Repair

# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "registration",
        "make",
        "model",
        "owner",
        "is_default",
    )

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle",
        "title",
        "priority",
        "status",
    )

    list_filter = (
        "priority",
        "status",
    )

    search_fields = (
        "title",
        "vehicle_registration", 
    )