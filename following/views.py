from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response

from .models import Following, CabangOlahraga
from .forms import FollowingForm, OlahragaForm
from main.models import CustomUser
from event.models import Event
from news.models import Berita
from comment.models import Comment

# Create your views here.
def createSportOnStart():
    tennis = CabangOlahraga(name="Tennis")
    swimming = CabangOlahraga(name="Swimming")
    athletic = CabangOlahraga(name="Athletic")
    basket = CabangOlahraga(name="Basket")
    other = CabangOlahraga(name="Other")

    tennisNotCreated = True
    swimmingNotCreated = True
    athleticNotCreated = True
    basketNotCreated = True
    otherNotCreated = True
    for sport in CabangOlahraga.objects.all().iterator():
        if sport.name == tennis.name: tennisNotCreated = False
        elif sport.name == swimming.name: swimmingNotCreated = False
        elif sport.name == athletic.name: athleticNotCreated = False
        elif sport.name == basket.name: basketNotCreated = False
        elif sport.name == other.name: otherNotCreated = False
    
    if (tennisNotCreated): tennis.save()
    if (swimmingNotCreated): swimming.save()
    if (athleticNotCreated): athletic.save()
    if (basketNotCreated): basket.save()
    if (otherNotCreated): other.save()

    for event in Event.objects.all():
        if (event.sport_branch == 'tennis'): event.cabangOlahraga = tennis
        elif (event.sport_branch == 'swim'): event.cabangOlahraga = swimming
        elif (event.sport_branch == 'atheltic'): event.cabangOlahraga = athletic
        elif (event.sport_branch == 'basket'): event.cabangOlahraga = basket
        else: event.cabangOlahraga = other

def createSportOnStart2():
    tennis = CabangOlahraga(name="Tennis")
    swimming = CabangOlahraga(name="Swimming")
    athletic = CabangOlahraga(name="Athletic")
    basket = CabangOlahraga(name="Basket")
    other = CabangOlahraga(name="Other")

    tennisNotCreated = True
    swimmingNotCreated = True
    athleticNotCreated = True
    basketNotCreated = True
    otherNotCreated = True
    for sport in CabangOlahraga.objects.all().iterator():
        if sport.name == tennis.name: tennisNotCreated = False
        elif sport.name == swimming.name: swimmingNotCreated = False
        elif sport.name == athletic.name: athleticNotCreated = False
        elif sport.name == basket.name: basketNotCreated = False
        elif sport.name == other.name: otherNotCreated = False
    
    if (tennisNotCreated): tennis.save()
    if (swimmingNotCreated): swimming.save()
    if (athleticNotCreated): athletic.save()
    if (basketNotCreated): basket.save()
    if (otherNotCreated): other.save()

    for news in Berita.objects.all():
        if ('tennis' in news.title.lower()) or ('tennis' in news.content.lower()): news.cabangOlahraga = tennis
        elif ('swim' in news.title.lower()) or ('swim' in news.content.lower()): news.cabangOlahraga = swimming
        elif ('athletic' in news.title.lower()) or ('athletic' in news.content.lower()): news.cabangOlahraga = athletic
        elif ('basket' in news.title.lower()) or ('basket' in news.content.lower()): news.cabangOlahraga = basket
        else: news.cabangOlahraga = other

def is_admin(user):
    return user.is_superuser

def getListOfEvents(user):
    createSportOnStart()
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    createSportOnStart2()
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

@login_required
def profilePage(request, userId):
    createSportOnStart()
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
                'sport_name': follow.cabangOlahraga.name
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
        
        following = Following.objects.all().filter(user = request.user)
        comment = Comment.objects.filter(user=request.user)
        event = Event.objects.filter(creator=request.user)
        news = Berita.objects.filter(author=request.user)

        threeRecentActivity = list(comment) + list(event)
        threeRecentActivity.sort(key=lambda x: x.created_at, reverse=True)
        threeRecentActivity = threeRecentActivity[:3]
        recentActivity = []
        for activity in threeRecentActivity:
            recentActivity.append({
                "content": activity,
                "type": activity.__class__.__name__,
            })

        followingCount = Following.objects.filter(user=request.user).count()
        commentCount = Comment.objects.filter(user=request.user).count()
        eventCount = Event.objects.filter(creator=request.user).count()
        is_admin = request.user.is_superuser

        return render(request, "profilePage.html", {
            "form": form,
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