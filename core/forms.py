# core/forms.py

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'size': '30',
        'aria-required': 'true',
        'placeholder': 'Nombre*',
        
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'size': '30',
        'aria-required': 'true',
        'placeholder': 'Email*',
    }))

    message = forms.CharField(widget=CKEditor5Widget(config_name="extends", attrs={
        'cols': '45',
        'rows': '8',
        'aria-required': 'true',
        'placeholder': 'Tu mensaje',
    }))