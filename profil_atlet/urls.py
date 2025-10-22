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
]