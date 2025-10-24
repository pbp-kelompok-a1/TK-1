from django.urls import path
from django.views.generic import RedirectView
from main.views import show_main
from main.views import register, login_user, logout_user, errorPage

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('error/', errorPage, name='error'),

    # Ini path harus terakhir ya ges ya
    path('<path:invalid_path>/', RedirectView.as_view(url='/error/', permanent=False)),
]