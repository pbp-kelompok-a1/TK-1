from django import forms
from .models import Following, CabangOlahraga

class FollowingForm(forms.ModelForm):
    class Meta:
        model = Following
        fields = ['cabangOlahraga']
        widgets = {'cabangOlahraga': forms.RadioSelect}

class OlahragaForm(forms.ModelForm):
    class Meta:
        model = CabangOlahraga
        fields = '__all__'