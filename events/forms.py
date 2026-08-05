from django import forms

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            "title",
            "venue",
            "event_date",
            "organiser",
            "vehicle",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }