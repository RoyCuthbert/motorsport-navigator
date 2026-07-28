from django.conf import settings
from django.db import models

# Create your models here.

class Vehicle(models.Model):

    DRIVE_TYPES = [
        ("FWD", "Front Wheel Drive"),
        ("RWD", "Rear Wheel Drive"),
        ("AWD", "All Wheel Drive"),
        ("4WD", "For Wheel Drive"),
    ]

    TRANSMISSION = [
        ("Manual", "Manual"),
        ("Automatic", "Automatic")
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="vehicles",    
    )

    registration = models.CharField(
        max_length=20,
        unique=True,    
    )

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    colour = models.CharField(max_length=50)
    engine_size = models.PositiveIntegerField()
    drive_type = models.CharField(
        max_length=10,
        choices = DRIVE_TYPES,
    )
    transmission = models.CharField(
            max_length=20,
            choices = TRANSMISSION,
    )
    logbook_number = models.CharField(
        max_length=100,
        blank=True,
    )
    mot_expiry = models.DateField(
        null = True,
        blank = True,
    )
    insurance_expiry = models.DateField(
        null = True,
        blank = True,
    )
    tax_expiry = models.DateField(
        null = True,
        blank = True,
    )
    image = models.ImageField(
        upload_to="vehicles/",
        blank=True,
        null=True,
    )

    is_default = models.BooleanField(
        default=False,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["make", "model"]

    def __str__(self):
        return f"{self.registration} - {self.make} {self.model}"