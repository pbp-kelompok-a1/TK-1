from django.forms import ModelForm
from main.models import Event, EventType

class EventForm(ModelForm):
    """
    ModelForm to handle creation of new Community Events.
    It excludes the 'event_type', 'creator', and 'id' fields, as they are
    set automatically or manually in the view logic.
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'official_link', 'start_time']