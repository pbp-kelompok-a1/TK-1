from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response

from .models import Following, CabangOlahraga
from .forms import FollowingForm, OlahragaForm
from main.models import CustomUser
from event.models import Event
from news.models import Berita
from comment.models import Comment

# Create your views here.
def getListOfEvents(user):
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-date'))

@login_required
def profilePage(request, userId):
    if (request.user == None): return redirect('main:login')
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            
            return JsonResponse({
                'success': True,
                'follow_id': follow.id,
                'sport_id': follow.cabangOlahraga.id,
                'sport_name': follow.cabangOlahraga.nama
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data'
            }, status=400)
    elif request.method == "POST":
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            return redirect('following:profile')
    else:
        form = FollowingForm()
        already_chosen = Following.objects.filter(user=request.user).values_list('cabangOlahraga', flat=True)
        form.fields['cabangOlahraga'].queryset = CabangOlahraga.objects.exclude(id__in=already_chosen)
        
        currentUser = CustomUser.objects.filter(user = request.user)
        profilePicture = currentUser.picture if hasattr(currentUser, 'picture') else None
        name = currentUser.name if hasattr(currentUser, 'name') else request.user.username
        username = currentUser.username if hasattr(currentUser, 'username') else request.user.username
        
        followingCount = Following.objects.filter(user=request.user).count()
        commentCount = Comment.objects.filter(user=request.user).count()
        eventCount = Event.objects.filter(creator=request.user).count()
        
        return render(request, "profilePage.html", {
            "form": form,
            "profilePicture": profilePicture,
            "name": name,
            "username": username,
            "followingCount": followingCount,
            "commentCount": commentCount,
            "eventCount": eventCount
        }, status=200)

@login_required
@require_POST
def unfollow(request, follow_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            follow = Following.objects.get(id=follow_id, user=request.user)
            sport_name = follow.cabangOlahraga.nama
            sport_id = follow.cabangOlahraga.id
            follow.delete()
            
            return JsonResponse({
                'success': True,
                'sport_id': sport_id,
                'sport_name': sport_name
            }, status=400)
        except Following.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Follow not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)