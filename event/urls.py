from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<uuid:event_id>/delete/', views.event_delete, name='event_delete'),
    path('create/global/', views.event_create_global, name='event_create_global'),
]