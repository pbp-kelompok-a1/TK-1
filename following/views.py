from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from models import Following
from event.models import Event

# Create your views here.

def compare(userLoggedIn, item1, item2):
    if (userLoggedIn != None):
        following = Following.objects.all()
        if (following.cabangOlahraga == item1.cabangOlahraga and following.cabangOlahraga != item2.cabangOlahraga):
            return -1
        elif (following.cabangOlahraga == item2.cabangOlahraga and following.cabangOlahraga != item1.cabangOlahraga):
            return 1
        else:
            if (item1.date > item2.date): 
                return -1
            else:
                return 1
    else:
        if (item1.date > item2.date): 
            return -1
        else:
            return 1
    
def getListOfEvents(events):
    sorted(events, key=compare)
    return events

# def getListOfNews(news):
#     sorted(news, key=compare)
#     return news

@api_view(['POST'])
def createFollowing(request):
    newFollowing = Following()
    newFollowing.save()
    return Response(status=status.HTTP_201_CREATED)