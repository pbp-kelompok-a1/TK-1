from django.urls import path
from . import views

app_name = 'news' # untuk namespacing

urlpatterns = [
    path('create-flutter/', views.create_news_flutter, name='create_news_flutter'),
    path('', views.berita_list, name='berita_list'),
    path('<int:pk>/', views.berita_detail, name='berita_detail'),
    path('add/', views.berita_create, name='berita_add'),
    path('<int:pk>/edit/', views.berita_edit, name='berita_edit'),
    path('<int:pk>/delete/', views.berita_delete, name='berita_delete'),
    path('json/', views.berita_json_list, name='json_list'),
    path('json/<int:pk>/', views.berita_json_detail, name='json_detail'),
    path('proxy-image/', views.proxy_image, name='proxy_image'),
    path('edit-flutter/<int:pk>/', views.edit_flutter, name='edit_flutter'),
    path('delete-flutter/<int:pk>/', views.delete_flutter, name='delete_flutter'),
    path('get-user-status/', views.get_user_status, name='get_user_status'),
]
