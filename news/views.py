from django.shortcuts import render, redirect, get_object_or_404
from .forms import BeritaForm
from .models import Berita
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def berita_list(request):
    if not request.user.is_authenticated:
        return redirect('/login/')   # <-- langsung lempar ke login

    berita = Berita.objects.all().order_by('-id')
    return render(request, 'news/berita_list.html', {'berita': berita})

def berita_detail(request, pk):
    item = get_object_or_404(Berita, pk=pk)
    return render(request, 'news/berita_detail.html', {'b': item})

def berita_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Login required.")
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed.")

    if request.method == "POST":
        form = BeritaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user      # otomatis
            obj.save()
            return redirect('berita_list')
    else:
        form = BeritaForm()

    return render(request, 'news/berita_form.html', {'form': form})

def berita_edit(request, pk):
    item = get_object_or_404(Berita, pk=pk)

    if request.user != item.author and not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed.")

    # Lanjut ke normal logic edit
    if request.method == "POST":
        form = BeritaForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('berita_detail', pk=pk)
    else:
        form = BeritaForm(instance=item)

    return render(request, 'news/berita_form.html', {'form': form})

def berita_delete(request, pk):
    item = get_object_or_404(Berita, pk=pk)

    if request.user != item.author and not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed.")

    item.delete()
    return redirect('berita_list')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login setelah signup
            return redirect('berita_list')
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', {'form': form})
