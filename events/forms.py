from django import forms

from .models import Event, EventTask


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["co_driver"].queryset = (
                self.fields["co_driver"]
                .queryset
                .filter(driver__user=user)
            )

    def clean(self):
        cleaned_data = super().clean()

        attendance_role = cleaned_data.get("attendance_role")

        if attendance_role and attendance_role != "Competitor":
            cleaned_data["vehicle"] = None
            cleaned_data["co_driver"] = None

        return cleaned_data

    class Meta:

        model = Event

        fields = [
            "title",
            "event_type",
            "attendance_role",
            "venue",
            "event_date",
            "organiser",
            "vehicle",
            "co_driver",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

class SharedEventSelectionForm(forms.Form):

    attendance_role = forms.ChoiceField(
        choices=Event.ATTENDANCE_ROLES,
        initial="Competitor",
        label="How are you attending?",
    )
    
class EventTaskForm(forms.ModelForm):

    class Meta:
        model = EventTask

        fields = [
            "title",
            "category",
            "priority",
            "due_date",
            "notes",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "priority": forms.Select(
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
                    "rows": 4,
                    "placeholder": "Optional notes...",
                }
            ),
        }