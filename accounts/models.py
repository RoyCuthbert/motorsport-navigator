from django.conf import settings
from django.db import models

# Create your models here.
class DriverProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "driver_profile"
    )

    # Personal Details

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    date_of_birth = models.DateField(blank = True, null = True,)

    # Contact Details

    email = models.EmailField()

    phone_number = models.CharField(max_length=14, blank = True)

    # Address

    address_line_1 = models.CharField(max_length=100)

    address_line_2 = models.CharField(
        max_length=100,
        blank=True
    )

    town = models.CharField(
        max_length=100,
        blank=True,
    )

    postcode = models.CharField(
        max_length=10,
        blank=True,
    )

    # Motorsport

    motorsport_uk_number = models.CharField(
        max_length=30,
        blank=True,
    )

    club_membership_number = models.CharField(
        max_length=30,
        blank=True
    )

    # Emergency Contact

    emergency_contact = models.CharField(max_length=100)

    emergency_phone = models.CharField(max_length=20)

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"