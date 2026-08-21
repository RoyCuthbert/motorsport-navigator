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

    review_notes = models.TextField(
        blank=True,
        help_text="Post-event notes, lessons learned, and improvements for future events.",
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

class EventTask(models.Model):

    CATEGORY_CHOICES = [
        ("Entry", "Entry"),
        ("Documents", "Documents"),
        ("Travel", "Travel"),
        ("Accommodation", "Accommodation"),
        ("Vehicle", "Vehicle"),
        ("Event", "Event"),
        ("Other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=200,
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Other",
    )


    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )

    completed = models.BooleanField(
        default=False,
    )

    due_date = models.DateField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def due_status(self):

        # Completed tasks take priority
        if self.completed:
            return "Completed"

        # No due date
        if not self.due_date:
            return "No Deadline"

        today = date.today()

        # Past due
        if self.due_date < today:
            return "Overdue"

        # Due today
        if self.due_date == today:
            return "Due Today"

        # Due within the next 7 days
        days_until_due = (self.due_date - today).days

        if days_until_due <= 7:
            return "Due Soon"

        # More than 7 days away
        return "Upcoming"

    class Meta:
        ordering = [
            "completed",
            "due_date",
            "created_at",
        ]

    def __str__(self):
        return self.title