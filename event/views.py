import json
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

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
    try:
        data = getListOfEvents(request.user)
    except:
        pass
    response_data = []

    for event in data:
        creator_info = {
            "id": event.creator.id if event.creator else 0,
            "username": event.creator.username if event.creator else "Anonymous"
        }
        
        response_data.append({
            "id": str(event.id),
            "title": event.title,
            "description": event.description,
            "sport_branch": event.sport_branch,
            "location": event.location if event.location else "",
            "picture_url": event.picture_url if event.picture_url else "",
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "event_type": event.event_type,
            "creator": {
                "id": event.creator.id if event.creator else 0,
                "username": event.creator.username if event.creator else "Unknown"
            },
            "cabangOlahraga": event.cabangOlahraga.id if event.cabangOlahraga else None,
            "created_at": event.created_at.isoformat(),
        })

    return JsonResponse(response_data, safe=False)


@csrf_exempt
@require_POST
def create_event_flutter(request):
    print("🔥 CREATE EVENT FLUTTER HIT 🔥") # DEBUG
    try:
        data = json.loads(request.body)

        assigned_type = (
            EventType.GLOBAL if request.user.is_staff else EventType.COMMUNITY
        )

        required_fields = ["title", "description", "start_time"]
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse(
                    {"status": "error", "message": f"Field '{field}' is required."},
                    status=400
                )

        parsed_start_time = parse_datetime(data["start_time"])
        if not parsed_start_time:
            return JsonResponse(
                {"status": "error", "message": "Invalid date format for start_time."},
                status=400
            )

        cabang_id = data.get("cabang_olahraga_id")
        cabang_obj = None
        if cabang_id:
            cabang_obj = get_object_or_404(CabangOlahraga, id=cabang_id)

        Event.objects.create(
            creator=request.user,
            title=data["title"],
            description=data["description"],
            location=data.get("location", ""),
            cabangOlahraga=cabang_obj,
            picture_url=data.get("picture_url", ""),
            start_time=parsed_start_time,
            event_type=assigned_type,
        )

        return JsonResponse(
            {"status": "success", "message": "Event created successfully!"},
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON payload."},
            status=400
        )


@csrf_exempt
@require_POST
def event_delete_flutter(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_staff or request.user == event.creator:
        event.delete()
        return JsonResponse({"status": "success", "message": "Event deleted successfully."})
    
    return JsonResponse({"status": "error", "message": "Access Denied."}, status=403)

@csrf_exempt
@require_POST
def edit_event_flutter(request, event_id):
    print("🔥 EDIT EVENT FLUTTER HIT 🔥")

    event = get_object_or_404(Event, id=event_id)

    if not (request.user.is_staff or request.user == event.creator):
        return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)

    data = json.loads(request.body)

    event.title = data["title"]
    event.description = data["description"]
    event.location = data.get("location", "")
    event.picture_url = data.get("picture_url", "")
    event.start_time = parse_datetime(data["start_time"])

    if data.get("cabang_olahraga_id"):
        event.cabangOlahraga = get_object_or_404(
            CabangOlahraga,
            id=data["cabang_olahraga_id"]
        )

    event.save()

    return JsonResponse({"status": "success"})