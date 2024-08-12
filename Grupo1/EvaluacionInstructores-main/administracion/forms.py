from django import forms
from .models import AccessTime

class AccessTimeForm(forms.ModelForm):
    class Meta:
        model = AccessTime
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }