from django import forms
from django.forms import ModelForm
from app_dole.models import (
    Profile,
)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname',
            'middlename',
            'surname',
            'ext_name',
            'date_of_birth',
            'gender',
            'civil_status',
            'purok_street',
            'contact_no',
            'barangay',
        ]
