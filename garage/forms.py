from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Vehicle


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        exclude = (
            "owner",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.add_input(
            Submit(
                "submit",
                "Save Vehicle",
                css_class="btn btn-danger w-100"
            )
        )