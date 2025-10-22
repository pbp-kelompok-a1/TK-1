from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from models import Event, EventType 
from forms import EventForm

from following.views import getListOfEvents

# Create your views here.
def event_list(request):

    upcoming_events = Event.objects.filter(
        start_time__gte=timezone.now()
    ).select_related('creator') 

    upcoming_events = getListOfEvents(upcoming_events)
    
    user_is_logged_in = request.user.is_authenticated
    is_admin = request.user.is_staff
    
    context = {
        'events': upcoming_events,
        'user_is_logged_in': user_is_logged_in,
        'is_admin': is_admin,
        
        'EVENT_TYPE_GLOBAL': EventType.GLOBAL,
        'EVENT_TYPE_COMMUNITY': EventType.COMMUNITY,
    }
    
    return render(request, 'events_list.html', context)

@login_required
def event_create(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create a Community Event.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.event_type = EventType.COMMUNITY 
            event.save()
            
            messages.success(request, f"Tournament '{event.title}' created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'page_title': "Create Community Tournament"
    }
    return render(request, 'event_create_form.html', context)
