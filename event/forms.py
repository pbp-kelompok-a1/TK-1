from django.utils import timezone
from django.core.exceptions import ValidationError
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'picture_url',
            'cabangOlahraga',
            'start_time',
            'end_time',
        ]
        DATETIME_INPUT_FORMAT = '%Y-%m-%dT%H:%M'
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format=DATETIME_INPUT_FORMAT
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format=DATETIME_INPUT_FORMAT
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DATETIME_INPUT_FORMAT = self.Meta.DATETIME_INPUT_FORMAT

        for field_name in ['start_time', 'end_time']:
            if field_name in self.fields:
                self.fields[field_name].input_formats = [DATETIME_INPUT_FORMAT]

        for field in self.fields.values():
            current_classes = field.widget.attrs.get('class', '')
            if not isinstance(field.widget, (forms.HiddenInput, forms.CheckboxInput)):
                field.widget.attrs['class'] = current_classes + ' django-input'
