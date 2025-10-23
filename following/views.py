from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Following

# Create your views here.

def compareEvent(userLoggedIn, item1, item2):
    if (userLoggedIn != None):
        following = Following.objects.all()
        currentDate = timezone.now()
        if (following.cabangOlahraga == item1.cabangOlahraga and item1.created_at == currentDate and following.cabangOlahraga != item2.cabangOlahraga):
            return -1
        elif (following.cabangOlahraga == item2.cabangOlahraga and item2.created_at == currentDate and following.cabangOlahraga != item1.cabangOlahraga):
            return 1
        else:
            if (item1.date > item2.date): 
                return -1
            elif (item1.date < item2.date): 
                return 1
            else:
                return 0
    else:
        if (item1.date > item2.date): 
            return -1
        elif (item1.date < item2.date): 
            return 1
        else:
            return 0
        
def compareNews(userLoggedIn, item1, item2):
    if (userLoggedIn != None):
        following = Following.objects.all()
        currentDate = timezone.now()
        if (following.cabangOlahraga == item1.cabangOlahraga and item1.date == currentDate and following.cabangOlahraga != item2.cabangOlahraga):
            return -1
        elif (following.cabangOlahraga == item2.cabangOlahraga and item2.date == currentDate and following.cabangOlahraga != item1.cabangOlahraga):
            return 1
        else:
            if (item1.date > item2.date): 
                return -1
            elif (item1.date < item2.date): 
                return 1
            else:
                return 0
    else:
        if (item1.date > item2.date): 
            return -1
        elif (item1.date < item2.date): 
            return 1
        else:
            return 0
    
def getListOfEvents(events):
    sorted(events, key=compareEvent)
    return events

def getListOfNews(news):
    sorted(news, key=compareNews)
    return news

@api_view(['POST'])
def createFollowing(request):
    newFollowing = Following()
    newFollowing.save()
    return Response(status=status.HTTP_201_CREATED)