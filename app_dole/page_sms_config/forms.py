from django import forms
from django.forms import ModelForm
from app_dole.models import (
    Sms_Config,
)


class Sms_ConfigForm(forms.ModelForm):
    class Meta:
        model = Sms_Config
        fields = [
            'ip_address',
            'username',
            'password',
        ]
