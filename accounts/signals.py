from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DriverProfile


@receiver(post_save, sender=User)
def create_driver_profile(sender, instance, created, **kwargs):

    if created:
        DriverProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_driver_profile(sender, instance, **kwargs):

    instance.driver_profile.save()