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
    path('edit-flutter/<uuid:event_id>/', views.edit_event_flutter, name='edit_event_flutter'),
    path('delete-flutter/<uuid:event_id>/', views.delete_event_flutter, name='delete_event_flutter'),
    path('create-flutter-global/', views.create_event_flutter_global, name='create_event_flutter_global'),
    path('user-status/', views.get_user_status, name='user_status'),
]
