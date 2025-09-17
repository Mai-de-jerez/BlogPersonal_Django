from django import forms
from .models import Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')
        widgets = {
            # Elimina el 'id' para que Django lo genere automáticamente
            'text': CKEditor5Widget(attrs={
                'cols': '45', 
                'rows': '8', 
                'aria-required': 'true', 
                'placeholder': 'Comentario*',
            }),

            # Elimina el 'id' para que Django lo genere automáticamente
            'name': forms.TextInput(attrs={
                'type': 'text', 
                'size': '30', 
                'aria-required': 'true', 
                'placeholder': 'Nombre*',
            }),
            # Elimina el 'id' para que Django lo genere automáticamente
            'email': forms.EmailInput(attrs={
                'type': 'text', 
                'size': '30', 
                'aria-required': 'true', 
                'placeholder': 'Email',
            }),

        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',) # Solo necesitamos el campo de texto
        widgets = {
            'text': CKEditor5Widget(attrs={
                'cols': '45',
                'rows': '3',
                'aria-required': 'true',
                'placeholder': 'Escribe tu respuesta...',
            }),
        }