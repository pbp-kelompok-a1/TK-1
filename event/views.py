from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import Event, EventType 
from .forms import EventForm


# Create your views here.
def event_list(request):
    upcoming_events = Event.objects.filter(
        start_time__gte=timezone.now()
    ).select_related('creator').order_by('start_time')
    
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
            response = redirect('event_list')

            storage = messages.get_messages(request)
            list(storage) 

            return response
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'page_title': "Create Community Tournament"
    }
    return render(request, 'event_create_form.html', context)

@login_required
def event_create_global(request):
    if not request.user.is_staff:
        messages.error(request, "Only admins can create Global Events.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.event_type = EventType.GLOBAL
            event.creator = request.user
            event.save()
            
            messages.success(request, f"Global Tournament '{event.title}' created successfully!")
            response = redirect('event_list')

            storage = messages.get_messages(request)
            list(storage) 

    else:
        form = EventForm()

    context = {
        'form': form,
        'page_title': "Create Global Tournament (Admin)"
    }
    return render(request, 'event_create_form.html', context)


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Only allow creator or admin
    if request.user == event.creator or request.user.is_staff:
        event.delete()
        messages.success(request, f'Event "{event.title}" deleted successfully.')
    else:
        messages.error(request, "You do not have permission to delete this event.")
    
    return redirect('event_list')
