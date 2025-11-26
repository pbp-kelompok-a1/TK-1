from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Event, EventType
from .forms import EventForm
from following.views import getListOfEvents

def event_list(request):
    user_is_logged_in = request.user.is_authenticated
    is_admin = request.user.is_staff

    upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).select_related('creator').order_by('start_time')
    if user_is_logged_in:
        try:
            upcoming_events = getListOfEvents(request.user).filter(start_time__gte=timezone.now())
        except:
            pass
    
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
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.event_type = EventType.COMMUNITY
            event.save()
            messages.success(request, f"Tournament '{event.title}' created successfully!")
            return redirect('event:event_list')
    else:
        form = EventForm()
    
    context = {'form': form, 'page_title': "Create Community Tournament"}
    return render(request, 'event_create_form.html', context)

@login_required
def event_create_global(request):
    if not request.user.is_staff:
        messages.error(request, "Only admins can create Global Events.")
        return redirect('event:event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.event_type = EventType.GLOBAL
            event.save()
            messages.success(request, f"Global Tournament '{event.title}' created successfully!")
            return redirect('event:event_list')
    else:
        form = EventForm()

    context = {'form': form, 'page_title': "Create Global Tournament (Admin)"}
    return render(request, 'event_create_form.html', context)

@login_required
@require_POST
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.creator or request.user.is_staff:
        title = event.title
        event.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'Event "{title}" deleted successfully.'})
        
        messages.success(request, f'Event "{title}" deleted successfully.')
        return redirect('event:event_list')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Permission denied.'}, status=403)
        messages.error(request, 'Permission denied.')
        return redirect('event:event_list')  
    
@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.creator and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this event.")
        return redirect('event:event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('event:event_list')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form, 
        'page_title': f"Edit Event: {event.title}"
    }
    
    return render(request, 'event_create_form.html', context)