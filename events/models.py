from django.conf import settings
from django.db import models
from datetime import date

EVENT_TYPES = [
        ("12 Car", "12 Car Rally"),
        ("Road Rally", "Road Rally"),
        ("Targa", "Targa Rally"),
        ("Autosolo", "Autosolo"),
        ("Autotest", "Autotest"),
        ("Production Car Trial", "Production Car Trial"),
        ("Sporting Trial", "Sporting Trial"),
        ("Stage Rally", "Stage Rally"),
        ("Hill Climb", "Hill Climb"),
        ("Sprint", "Sprint"),
        ("Track Day", "Track Day"),
        ("Test Day", "Test Day"),
        ("Navigational Scatter", "Scatter Rally"),
        ("Treasure Hunt", "Treasure Hunt"),
        ("Social", "Club Social"),
        ("Training", "Training"),
        ("Other", "Other"),
    ]


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

    event_type = models.CharField(
            max_length=50,
            choices=EVENT_TYPES,
            default="Road Rally",
    )

    organiser = models.CharField(
        max_length=100,
        blank=True,
    )

    venue = models.CharField(max_length=100)

    event_date = models.DateField()

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
        return (self.event_date - date.today()).days