from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Vehicle, Repair


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

class RepairForm(forms.ModelForm):

    class Meta:
        model = Repair
        fields = [
            "vehicle",
            "title",
            "description",
            "priority",
            "status",
            "estimated_cost",
        ]