from django import forms
from .models import DriverProfile


class DriverProfileForm(forms.ModelForm):

    class Meta:

        model = DriverProfile

        exclude = (
            "user",
            "created_on",
            "updated_on",
        )