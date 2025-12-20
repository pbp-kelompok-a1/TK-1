from django.urls import path
from . import views 

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<uuid:event_id>/delete/', views.event_delete, name='event_delete'),
    path('create/global/', views.event_create_global, name='event_create_global'),
    path('<uuid:event_id>/edit/', views.event_edit, name='event_edit'),
    path('json/', views.show_json, name='show_json'),
    path('create-flutter/', views.create_event_flutter, name='create_event_flutter'),
]