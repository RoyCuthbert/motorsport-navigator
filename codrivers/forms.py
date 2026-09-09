from django import forms

from .models import CoDriverProfile


class CoDriverProfileForm(forms.ModelForm):

    class Meta:
        model = CoDriverProfile

        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "town",
            "postcode",
            "motorsport_uk_number",
            "club_membership_number",
            "bio",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }