from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('profile/', profilePage, name='profile'),
    path('unfollow/<uuid:follow_id>/', unfollow, name='unfollow'),
    path('createSport/', createCabangOlahraga, name='createSport'),
    path('showJSONFollowing/', getJSONFollowing, name='showJSONFollowing'),
    path('showJSONCabangOlahraga/', getJSONCabangOlahraga, name='showJSONCabangOlahraga'),
    path('showJSONCustomUser/', getJSONCustomUser, name='showJSONCustomUser'),
    path('getProfilePictureURLs/', getProfilePictureURLs, name='getProfilePictureURLs'),
    path('currentUser/', getCurrentUser, name='currentUser'),
    path('users/', getUsers, name='users'),
    path('profile2/', profilePage2, name='profile2'),
    path('unfollow2/<uuid:follow_id>/', unfollow2, name='unfollow2')
]