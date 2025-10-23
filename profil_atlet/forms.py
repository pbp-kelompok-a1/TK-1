from django import forms
from .models import Atlet

INPUT_DATE_FORMATS = [
    '%Y-%m-%d',    # YYYY-MM-DD 
    '%d/%m/%Y',    # DD/MM/YYYY 
    '%d-%m-%Y',    # DD-MM-YYYY 
]

class AtletForm(forms.ModelForm):
    
    birth_date = forms.DateField(
        label='Birth date',
        # tentuin widget dan format yang akan kita izinkan untuk diinput pengguna
        widget=forms.TextInput(
            attrs={
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off' 
            }
        ),
        input_formats=INPUT_DATE_FORMATS, 
        required=False # pastikan ini wajib diisi
    )
    
    class Meta:
        model = Atlet
        # tampilkan semua field di form Admin
        fields = '__all__'