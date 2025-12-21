# ini utk file profil_atlet/urls.py
from django.urls import path
from . import views

app_name = 'profil_atlet' # untuk namespacing

urlpatterns = [
    # URL untuk Read (List dan Detail)
    path('', views.list_atlet, name='list_atlet'),
    path('<int:pk>/', views.detail_atlet, name='detail_atlet'),
    
    # URL untuk Create, Update, Delete (Admin)
    path('create/', views.create_atlet, name='create_atlet'),
    path('update/<int:pk>/', views.update_atlet, name='update_atlet'),
    path('delete/<int:pk>/', views.delete_atlet, name='delete_atlet'),
    path('json/', views.show_json_atlet, name='show_json_atlet'),
    path('create-ajax/', views.create_atlet_ajax, name='create_atlet_ajax'),
    path('delete-ajax/<int:pk>/', views.delete_atlet_ajax, name='delete_atlet_ajax'),
    
    path('<int:atlet_pk>/add_medal/', views.create_medali, name='create_medali'),
    path('update_medal/<int:medal_pk>/', views.update_medali, name='update_medali'),
    path('delete_medal/<int:medal_pk>/', views.delete_medali, name='delete_medali'),
    path('json-detail/<int:pk>/', views.show_json_detail_atlet, name='show_json_detail_atlet'),
    path('create-flutter/', views.create_atlet_flutter, name='create_atlet_flutter'),
    path('edit-flutter/<int:pk>/', views.edit_atlet_flutter, name='edit_atlet_flutter'),
    
    path('edit-medali-flutter/<int:pk>/', views.edit_medali_flutter, name='edit_medali_flutter'),
    path('delete-medali-flutter/<int:pk>/', views.delete_medali_flutter, name='delete_medali_flutter'),
    path('add-medali-flutter/<int:atlet_pk>/', views.add_medali_flutter, name='add_medali_flutter'),
]