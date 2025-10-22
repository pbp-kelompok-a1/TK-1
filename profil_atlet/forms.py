# profil_atlet/forms.py
from django import forms
from .models import Atlet

class AtletForm(forms.ModelForm):
    class Meta:
        model = Atlet
        # tampilkan semua field di form Admin
        fields = '__all__'