import json
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from following.models import CabangOlahraga

from .models import Event, EventType, SportBranch
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

def show_json(request):
    data = Event.objects.all()
    response_data = []

    for event in data:
        response_data.append({
            "id": str(event.id),
            "title": event.title,
            "description": event.description,
            "sport_branch": event.sport_branch,
            "location": event.location,
            "picture_url": event.picture_url,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "event_type": event.event_type,
            "creator": event.creator.id if event.creator else None,
            "cabangOlahraga": event.cabangOlahraga.id if event.cabangOlahraga else None,
            "created_at": event.created_at.isoformat(),
        })

    return JsonResponse(response_data, safe=False)

@csrf_exempt
def create_event_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            new_event = Event.objects.create(
                creator=request.user,
                title = data["title"],
                description = data["description"],
                sport_branch = data.get("sport_branch", SportBranch.OTHER),
                location = data.get("location", ""),    
                picture_url = data.get("picture_url", ""),
                start_time = data["start_time"],
                end_time = data.get("end_time", None),
                event_type = data.get("event_type", EventType.COMMUNITY),
            )
            
            new_event.save()
            
            return JsonResponse({"status": "success", "message": "Event created successfully."}, status=201)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
def create_event_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cabang_id = data.get("cabag_olahraga_id")
            
            if cabang_id:
                cabang_olahraga_obj = CabangOlahraga.objects.get(id=cabang_id)
            else: 
                cabang_olahraga_obj = None
                
            new_event = Event.objects.create(
                creator=request.user,
                
                title=data["title"],
                description = data["description"],
                location = data.get("location", ""),
                
                cabangOlahraga = cabang_olahraga_obj,
                
                picture_url = data.get("picture_url", ""),
                
                start_time = parse_datetime(data["start_time"]),
                
                event_type = "community",
            )
            
            new_event.save()
            return JsonResponse({"status": "success", "message": "Event berhasil dibuat!"}, status=200)

        except CabangOlahraga.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cabang Olahraga tidak ditemukan."}, status=404)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Metode request tidak valid."}, status=401)