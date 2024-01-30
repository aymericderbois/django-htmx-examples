from django import forms

from apps.calendar.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "start")

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "My event"}
            ),
            "start": forms.DateTimeInput(attrs={"class": "form-control datepicker"}),
        }
