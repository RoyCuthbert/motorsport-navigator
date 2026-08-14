from django import forms

from .models import Event, EventTask


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            "title",
            "event_type",
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

class EventTaskForm(forms.ModelForm):

    class Meta:
        model = EventTask

        fields = [
            "title",
            "category",
            "due_date",
            "notes",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Submit event entry",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional notes...",
                }
            ),
        }