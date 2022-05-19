from django import forms
from django.forms import ModelForm
from app_dole.models import (
    Programs,
    Sms_Bluster
)

class ProgramsForm(forms.ModelForm):
    class Meta:
        model = Programs
        fields = [
            'description',
            'sponsored_by',
            'category',
            'date_from',
            'date_to',
        ]

class Sms_BlusterForm(forms.ModelForm):
    message = forms.CharField(
                            label="",
                            widget=forms.Textarea(
                                attrs=
                                    {'rows': 3,'style' : "white-space: pre-wrap",'placeholder': "Send a message"},
                                ),
                            )
    class Meta:
        model = Sms_Bluster
        fields = [
            'message',
        ]
