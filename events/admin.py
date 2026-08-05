from django.contrib import admin
from .models import Event

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_date",
        "venue",
        "vehicle",
        "status",
        "selected",
    )

    list_filter = (
        "status",
        "selected",
    )

    search_fields = (
        "title",
        "venue",
        "organiser",
    )