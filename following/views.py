from django.shortcuts import render
from django.utils import timezone
from django.db.models import Exists, OuterRef
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Following
from event.models import Event
from news.models import Berita

# Create your views here.
def getListOfEvents(user):
    followed_sports = Following.objects.filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    followed_sports = Following.objects.filter(user=user, sport_type=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-date'))

@api_view(['POST'])
def createFollowing(request):
    newFollowing = Following()
    newFollowing.save()
    return Response(status=status.HTTP_201_CREATED)