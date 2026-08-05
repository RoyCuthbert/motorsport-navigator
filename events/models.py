from django.conf import settings
from django.db import models
from django.utils import timezone


class Event(models.Model):

    EVENT_STATUS = [
        ("Upcoming", "Upcoming"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    vehicle = models.ForeignKey(
        "garage.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=100)

    organiser = models.CharField(
        max_length=100,
        blank=True,
    )

    venue = models.CharField(max_length=100)

    event_date = models.DateField()

    event_type = models.CharField(
        max_length=50,
        default="Rally",
    )

    status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS,
        default="Upcoming",
    )

    selected = models.BooleanField(
        default=False,
    )

    notes = models.TextField(
        blank=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return self.title

@property
def days_remaining(self):
    delta = self.event_date - timezone.now().date()
    return delta.days