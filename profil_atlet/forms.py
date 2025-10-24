from django import forms
from .models import Atlet
from django.utils.html import strip_tags

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
        
    def clean_name(self):
        data = self.cleaned_data.get('name')
        if data:
            return strip_tags(data)
        return data

    def clean_short_name(self):
        data = self.cleaned_data.get('short_name')
        if data:
            return strip_tags(data)
        return data

    def clean_country(self):
        data = self.cleaned_data.get('country')
        if data:
            return strip_tags(data)
        return data

    def clean_discipline(self):
        data = self.cleaned_data.get('discipline')
        if data:
            return strip_tags(data)
        return data

    def clean_gender(self):
        data = self.cleaned_data.get('gender')
        if data:
            return strip_tags(data)
        return data

    def clean_birth_place(self):
        data = self.cleaned_data.get('birth_place')
        if data:
            return strip_tags(data)
        return data

    def clean_birth_country(self):
        data = self.cleaned_data.get('birth_country')
        if data:
            return strip_tags(data)
        return data
    
    def clean_nationality(self):
        data = self.cleaned_data.get('nationality')
        if data:
            return strip_tags(data)
        return data