from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status

from .models import Following, CabangOlahraga
from .forms import FollowingForm, OlahragaForm
from main.models import CustomUser
from event.models import Event
from news.models import Berita

# Create your views here.
def getListOfEvents(user):
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    followed_sports = Following.objects.all().filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-date'))

@login_required(login_url='/login')
def profilePage(request):
    if (request.method == "POST"):
        form = FollowingForm(request.POST)
        if (form.is_valid()):
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            return redirect('following:profile')
    else :
        form = FollowingForm()

        already_chosen = Following.objects.filter(user=request.user).values_list('cabangOlahraga', flat=True)
        form.fields['cabangOlahraga'].queryset = CabangOlahraga.objects.exclude(id__in=already_chosen)

        currentUser = CustomUser.objects.filter(user = request.user)
        profilePicture = currentUser.picture
        name = currentUser.name
        username = currentUser.username

        following = Following.objects.filter(user = request.user)

        return render(request, "profilePage.html", {"form": form, "profilePicture": profilePicture, "name": name, "username": username, "following": following})