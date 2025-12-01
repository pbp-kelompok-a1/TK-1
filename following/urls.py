from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('profile/<int:userId>', profilePage, name='profile'),
    path('unfollow/<uuid:follow_id>/', unfollow, name='unfollow'),
    path('createSport/', createCabangOlahraga, name='createSport'),
    path('showJSONFollowing/', getJSONFollowing, name='showJSONFollowing'),
    path('showJSONCabangOlahraga/', getJSONCabangOlahraga, name='showJSONCabangOlahraga'),
    path('showJSONCustomUser/', getJSONCustomUser, name='showJSONCustomUser'),
]