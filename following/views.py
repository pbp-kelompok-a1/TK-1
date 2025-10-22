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
        if (following.user == item1.user and following.user != item2.user):
            return -1
        elif (following.user == item2.user and following.user != item1.user):
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

# @api_view(['GET'])
# def getListOfNews(request):
#     news = News.objects.all()
#     sorted(news, key=compare)
#     return Response({'news': news}, status=status.HTTP_200_OK)

@api_view(['POST'])
def createFollowing(request):
    newFollowing = Following()
    newFollowing.save()
    return Response(status=status.HTTP_201_CREATED)