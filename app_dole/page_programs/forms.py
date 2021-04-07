from django import forms
from django.forms import ModelForm
from app_dole.models import (
    Programs,
)

class ProgramsForm(forms.ModelForm):
    class Meta:
        model = Programs
        fields = [
            'description',
            'sponsored_by',
            'date_from',
            'date_to',
        ]
