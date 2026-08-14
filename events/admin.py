from django.contrib import admin
from .models import Event, EventTask

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

    @admin.register(EventTask)
    class EventTaskAdmin(admin.ModelAdmin):

        list_display = (
            "title",
            "event",
            "category",
            "completed",
            "due_date",
        )

        list_filter = (
            "category",
            "completed",
            "event",
        )

        search_fields = (
            "title",
            "event__title",
        )