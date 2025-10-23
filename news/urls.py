from django.urls import path
from . import views

app_name = 'news' # untuk namespacing

urlpatterns = [
    path('', views.berita_list, name='berita_list'),
    path('<int:pk>/', views.berita_detail, name='berita_detail'),
    path('add/', views.berita_create, name='berita_add'),
    path('<int:pk>/edit/', views.berita_edit, name='berita_edit'),
    path('<int:pk>/delete/', views.berita_delete, name='berita_delete'),
]
