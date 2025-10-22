from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('berita_list')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('berita/', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
