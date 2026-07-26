from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DriverProfile(models.Model):
    user = models.OneToOneField(
        User,
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

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    # Emergency Contact

class EmergencyContact(models.Model):

    profile = models.OneToOneField(
        DriverProfile,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    relationship = models.CharField(max_length=50)

    phone = models.CharField(max_length=20)

    alternative_phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.name