from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from news.models import Berita
from event.models import Event
from profil_atlet.models import Atlet

from .models import CustomUser
from .forms import CustomUserUpdateForm

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            newUser = CustomUser(user=user, username=user.username, name=user.username, join_date=datetime.datetime.now())
            newUser.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

def show_main(request):
    # Ambil 3–5 berita terbaru
    top_news = Berita.objects.all().order_by('-id')[:10]
    upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:10]
    top_athletes = Atlet.objects.filter(is_visible=True).order_by('id')[:10]

    context = {
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'top_news': top_news,
        'upcoming_events': upcoming_events,
        'featured_athletes':top_athletes,
    }
    return render(request, "main.html", context)

def errorPage(request):
    return render(request, "error.html")

@login_required
def update_atlet(request, pk):
    customUser = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=customUser)
        if form.is_valid():
            form.save()
            return redirect('profil_atlet:detail_atlet', pk=customUser.pk) 
    else:
        form = CustomUserUpdateForm(instance=customUser)
        
    context = {'form': form, 'back_url': reverse('profil_atlet:detail_atlet', args=[customUser.pk])}
    return render(request, 'profil_atlet/form_atlet.html', context)
