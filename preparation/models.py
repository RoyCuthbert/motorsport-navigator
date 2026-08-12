from django.conf import settings
from django.db import models

from events.models import Event

# Create your models here.
class PreparationItem(models.Model):

    CATEGORY_CHOICES = [
        ("Vehicle", "Vehicle Checks"),
        ("Safety", "Safety Equipment"),
        ("Documents", "Documents"),
        ("Tools", "Tools & Spares"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="preparation_items",
        null=True,
        blank=True,
     )

    vehicle = models.ForeignKey(
        "garage.Vehicle",
        on_delete=models.CASCADE,
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    item = models.CharField(
        max_length=100,
    )

    completed = models.BooleanField(
        default=False,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "category",
            "item",
        ]

    def __str__(self):
        return self.item