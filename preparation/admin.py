from django.contrib import admin

from .models import PreparationItem

# Register your models here.
@admin.register(PreparationItem)
class PreparationItemAdmin(admin.ModelAdmin):

    list_display = (
        "item",
        "category",
        "vehicle",
        "completed",
    )

    list_filter = (
        "category",
        "completed",
    )

    search_fields = (
        "item",
    )