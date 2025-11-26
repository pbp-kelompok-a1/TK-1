from django import forms
from .models import CustomUser

class CustomUserUpdateForm(forms.ModelForm):
    """Simplified form for updating only the name"""
    
    class Meta:
        model = CustomUser
        fields = ['name', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }