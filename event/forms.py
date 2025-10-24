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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        now = timezone.now()


        if start_time and start_time < now:
            self.add_error('start_time', ValidationError("Start time cannot be in the past."))


        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', ValidationError("End time must be after start time."))

        return cleaned_data

    def setUp(self):
        # Sample CabangOlahraga instance (adjust field name to match your model)
        self.cabang = CabangOlahraga.objects.create(namaCabang="Para Swimming")

        # Common valid datetime values
        self.now = timezone.now()
        self.future_start = self.now + timedelta(days=1)
        self.future_end = self.future_start + timedelta(hours=2)

        # Common valid form data
        self.valid_data = {
            "title": "ParaWorld Championship",
            "description": "An international para-sports event.",
            "location": "Jakarta",
            "picture_url": "https://example.com/image.jpg",
            "cabangOlahraga": self.cabang.id,
            "start_time": self.future_start.strftime("%Y-%m-%dT%H:%M"),
            "end_time": self.future_end.strftime("%Y-%m-%dT%H:%M"),
        }

    def test_valid_form(self):
        """Form should be valid with correct future datetimes."""
        form = EventForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_start_time_in_past(self):
        """Form should reject past start_time."""
        past_start = self.now - timedelta(days=1)
        data = self.valid_data.copy()
        data["start_time"] = past_start.strftime("%Y-%m-%dT%H:%M")
        form = EventForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("start_time", form.errors)
        self.assertIn("Start time cannot be in the past.", form.errors["start_time"][0])

    def test_end_time_before_start_time(self):
        """Form should reject when end_time <= start_time."""
        data = self.valid_data.copy()
        data["end_time"] = self.future_start.strftime("%Y-%m-%dT%H:%M")  # same as start
        form = EventForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("end_time", form.errors)
        self.assertIn("End time must be after start time.", form.errors["end_time"][0])

    def test_optional_fields_can_be_blank(self):
        """Optional fields like location and picture_url can be blank."""
        data = self.valid_data.copy()
        data["location"] = ""
        data["picture_url"] = ""
        form = EventForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_datetime_widget_type(self):
        """Check that datetime fields use type='datetime-local' in widgets."""
        form = EventForm()
        self.assertEqual(form.fields["start_time"].widget.attrs.get("type"), "datetime-local")
        self.assertEqual(form.fields["end_time"].widget.attrs.get("type"), "datetime-local")