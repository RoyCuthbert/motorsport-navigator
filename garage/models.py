from datetime import date
from django.conf import settings
from django.db import models

# Create your models here.

class Vehicle(models.Model):

    DRIVE_TYPES = [
        ("FWD", "Front Wheel Drive"),
        ("RWD", "Rear Wheel Drive"),
        ("AWD", "All Wheel Drive"),
        ("4WD", "Four Wheel Drive"),
    ]

    TRANSMISSION = [
        ("Manual", "Manual"),
        ("Automatic", "Automatic")
    ]

    FUEL_TYPES = [
    ("Petrol", "Petrol"),
    ("Diesel", "Diesel"),
    ("Electric", "Electric"),
    ("Hybrid", "Hybrid"),
]

    VEHICLE_CLASS = [
        ("Road", "Road"),
        ("Historic", "Historic"),
        ("Autotest", "Autotest"),
        ("Autosolo", "Autosolo"),
        ("Targa", "Targa"),
        ("Stage", "Stage"),
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

    nickname = models.CharField(max_length=50)
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
    vehicle_class = models.CharField(
        max_length=20,
        choices=VEHICLE_CLASS,
        default="Road",
    )
    
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPES,
        default="Petrol",
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
    vehicle_image = models.ImageField(
        upload_to="garage/",
        blank=True,
        null=True,
    )

    active = models.BooleanField(
        default=True,
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

    @property
    def insurance_valid(self):
        if self.insurance_expiry:
            return self.insurance_expiry >= date.today()
        return False
    
    
    @property
    def mot_valid(self):
        if self.mot_expiry:
            return self.mot_expiry >= date.today()
        return False
    
    @property
    def tax_valid(self):
        if self.tax_expiry:
            return self.tax_expiry >= date.today()
        return False

    from datetime import date

    def __str__(self):
        return f"{self.registration} - {self.make} {self.model}"
