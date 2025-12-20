from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('json/<int:news_id>/', views.show_json, name='show_json'),
    path('add/<int:news_id>/', views.add_comment, name='add_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add_flutter/<int:news_id>/', views.add_comment_flutter, name='add_comment_flutter'),
    path('edit_flutter/<int:comment_id>/', views.edit_comment_flutter, name='edit_comment_flutter'),
    path('delete_flutter/<int:comment_id>/', views.delete_comment_flutter, name='delete_comment_flutter'),
]
