from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Vehicle
# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):

    list_display = (
        "registration",
        "make",
        "model",
        "owner",
        "is_default",
    )

    search_fields = (
        "registration",
        "make",
        "model",
    )

    list_filter = (
        "make",
        "drive_type",
        "transmission",
    )