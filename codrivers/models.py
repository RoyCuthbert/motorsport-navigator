from django.db import models

from accounts.models import DriverProfile
# Create your models here.
class CoDriverProfile(models.Model):
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name="codrivers",
    )

    # Personal Details

    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    # Contact Details

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=14,
        blank=True,
    )

    # Address

    address_line_1 = models.CharField(
        max_length=100,
        blank=True,
    )

    address_line_2 = models.CharField(
        max_length=100,
        blank=True,
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
        blank=True,
    )

    # Profile

    bio = models.TextField(
        blank=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or f"Co-driver for {self.driver}"

class CoDriverEmergencyContact(models.Model):
    profile = models.OneToOneField(
        CoDriverProfile,
        on_delete=models.CASCADE,
        related_name="emergency_contact",
    )

    name = models.CharField(
        max_length=100,
    )

    relationship = models.CharField(
        max_length=50,
    )

    phone = models.CharField(
        max_length=20,
    )

    alternative_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return self.name