from datetime import date
from django.conf import settings
from django.db import models
from django.db.models import Sum

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
        ordering = ["-is_default","make", "model"]

    @property
    def insurance_days_remaining(self):

        if not self.insurance_expiry:
            return None

        return (self.insurance_expiry - date.today()).days
    
    
    @property
    def mot_days_remaining(self):

        if not self.mot_expiry:
            return None

        return (self.mot_expiry - date.today()).days
    
    @property
    def tax_days_remaining(self):

        if not self.tax_expiry:
            return None

        return (self.tax_expiry - date.today()).days

    @property
    def mot_valid(self):

        if self.mot_expiry:
            return self.mot_expiry >= date.today()

        return False


    @property
    def insurance_valid(self):

        if self.insurance_expiry:
            return self.insurance_expiry >= date.today()

        return False


    @property
    def tax_valid(self):

        if self.tax_expiry:
            return self.tax_expiry >= date.today()

        return False

    @property
    def minor_repairs(self):
        return self.repairs.filter(
            priority="Minor",
            status="Outstanding"
        ).count()
    
    
    @property
    def major_repairs(self):
        return self.repairs.filter(
            priority="Major",
            status="Outstanding"
        ).count()
    
    
    @property
    def critical_repairs(self):
        return self.repairs.filter(
            priority="Critical",
            status="Outstanding"
        ).count()

    @property
    def outstanding_repairs(self):
        return self.repairs.filter(
            status="Outstanding"
        ).count()

    @property
    def repair_cost(self):

        total = self.repairs.filter(
            status="Outstanding"
        ).aggregate(
            Sum("estimated_cost")
        )["estimated_cost__sum"]

        return total or 0
    
    @property
    def readiness_score(self):
    
        score = 100
    
        score -= self.minor_repairs * 3
        score -= self.major_repairs * 10
        score -= self.critical_repairs * 25

        if not self.mot_valid:
            score -= 20

        if not self.insurance_valid:
            score -= 20

        if not self.tax_valid:
            score -= 15
    
        return max(score, 0)

    @property
    def competition_ready(self):
        return self.readiness_score >= 80

    @property
    def competition_status(self):

        # Road vehicles must be legal to use
        if self.vehicle_class == "Road":

            if (
                not self.mot_valid
                or not self.insurance_valid
                or not self.tax_valid
            ):
                 return "NOT READY"

        # Critical repairs always make the vehicle not ready
        if self.critical_repairs > 0:
            return "NOT READY"

        # Minor or major repairs mean attention is needed
        if (
            self.major_repairs > 0
            or self.minor_repairs > 0
            or self.readiness_score < 80
        ):
            return "NEEDS ATTENTION"

        return "READY"

    def __str__(self):
        return f"{self.registration} - {self.make} {self.model}"

class Repair(models.Model):

    REPAIR_LEVELS = [
        ("Critical", "Critical"),
        ("Major", "Major"),
        ("Minor", "Minor"),
        ("Advisory", "Advisory"),
    ]

    STATUS = [
        ("Outstanding", "Outstanding"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="repairs",
    )

    title = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    priority = models.CharField(
        max_length=20,
        choices=REPAIR_LEVELS,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Outstanding",
    )

    estimated_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    reported_on = models.DateTimeField(
        auto_now_add=True,
    )

    completed_on = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["status", "-reported_on"]

    def __str__(self):
        return self.title