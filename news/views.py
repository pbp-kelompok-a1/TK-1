from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BeritaForm
from .models import Berita

from following.views import getListOfNews

def berita_list(request):
    berita = Berita.objects.all().order_by('-id')
    if request.user != None:
        try:
            berita = getListOfNews(request.user)
        except:
            berita = berita

    # berita = getListOfNews(berita)
    return render(request, 'news/berita_list.html', {'berita': berita})

def berita_detail(request, pk):
    item = get_object_or_404(Berita, pk=pk)
    return render(request, 'news/berita_detail.html', {'b': item})

@login_required(login_url='/login')
def berita_create(request):
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
    item.delete()
    return redirect('berita_list')
