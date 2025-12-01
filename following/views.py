from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Following, CabangOlahraga
from .forms import FollowingForm, OlahragaForm
from main.models import CustomUser
from main.forms import CustomUserUpdateForm
from event.models import Event
from news.models import Berita
from comment.models import Comment

# Create your views here.
def checkNewsCabangOlahraga():
    for berita in Berita.objects.all():
        for cabor in CabangOlahraga.objects.all():
            if cabor.name.lower() in berita.title.lower() or cabor.name.lower() in berita.content.lower():
                berita.cabangOlahraga = cabor
                berita.save()
                break

def is_admin(user):
    return user.is_superuser

def getListOfEvents(user):
    followed_sports = Following.objects.all().filter(user=user, cabangOlahraga=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    checkNewsCabangOlahraga()
    followed_sports = Following.objects.all().filter(user=user, cabangOlahraga=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

@login_required
@require_POST
@csrf_exempt
def unfollow(request, follow_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            follow = Following.objects.get(id=follow_id, user=request.user)
            sport_name = follow.cabangOlahraga.name
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

def createCabangOlahraga(request):
    if (request.method == 'GET'):
        form = OlahragaForm()
        context = {'form': form,'page_title': 'Add Sport'}
        return render(request, 'cabangOlahragaCreationPage.html', context)
    else:
        form = OlahragaForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('main:show_main')
        
@login_required
def profilePage(request, userId):
    # Handle profile picture/name update (AJAX)
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Check if it's a CustomUser update request
        if 'update_profile' in request.POST or request.FILES:
            try:
                custom_user = CustomUser.objects.get(user=request.user)
                form = CustomUserUpdateForm(request.POST, request.FILES, instance=custom_user)
                
                if form.is_valid():
                    updated_user = form.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'data': {
                            'name': updated_user.name,
                            'picture': updated_user.picture.url if updated_user.picture else None
                        }
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Validation failed',
                        'errors': form.errors
                    }, status=400)
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'User profile not found'
                }, status=404)
        
        # Handle following sport (existing code)
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            
            return JsonResponse({
                'success': True,
                'follow_id': str(follow.id),
                'sport_id': str(follow.cabangOlahraga.id),
                'sport_name': follow.cabangOlahraga.name
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data'
            }, status=400)
    
    elif request.method == "POST":
        # Handle non-AJAX POST
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            return redirect('profile', userId=userId)
    
    else:
        # GET request - display profile
        form = FollowingForm()
        already_chosen = Following.objects.filter(user=request.user).values_list('cabangOlahraga', flat=True)
        form.fields['cabangOlahraga'].queryset = CabangOlahraga.objects.exclude(id__in=already_chosen)
        
        # Get or create CustomUser
        try:
            currentUser = CustomUser.objects.get(user=request.user)
        except CustomUser.DoesNotExist:
            currentUser = CustomUser.objects.create(
                user=request.user,
                username=request.user.username,
                name=request.user.username
            )
        
        profilePicture = currentUser.picture if currentUser.picture else None
        name = currentUser.name if currentUser.name else request.user.username
        username = currentUser.username
        
        following = Following.objects.all().filter(user=request.user)
        comment = Comment.objects.filter(user=request.user)
        event = Event.objects.filter(creator=request.user)
        news = Berita.objects.filter(author=request.user)

        threeRecentActivity = list(comment) + list(event)
        threeRecentActivity.sort(key=lambda x: x.created_at, reverse=True)
        threeRecentActivity = threeRecentActivity[:3]
        recentActivity = []
        for activity in threeRecentActivity:
            recentActivity.append({
                "object": activity,
                "type": activity.__class__.__name__,
            })

        followingCount = Following.objects.filter(user=request.user).count()
        commentCount = Comment.objects.filter(user=request.user).count()
        eventCount = Event.objects.filter(creator=request.user).count()
        is_admin = request.user.is_superuser
        
        # Profile update form
        profile_form = CustomUserUpdateForm(instance=currentUser)

        return render(request, "profilePage.html", {
            "form": form,
            "profile_form": profile_form,
            "profilePicture": profilePicture,
            "name": name,
            "username": username,
            "following": following,
            "followingCount": followingCount,
            "commentCount": commentCount,
            "eventCount": eventCount,
            "is_admin": is_admin,
            "recentActivity": recentActivity
        }, status=200)