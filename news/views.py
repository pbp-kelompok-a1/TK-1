from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BeritaForm
from .models import Berita
from following.views import getListOfNews
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

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
            obj.author = request.user
            obj.save()
            return JsonResponse({
                "status": "ok",
                "id": obj.id,
                "title": obj.title,
                "thumbnail": obj.thumbnail or "",
                "category": obj.get_category_display(),
                "url_detail": reverse('news:berita_detail', args=[obj.id]),
            })
        return JsonResponse({"status": "error","errors": form.errors}, status=400)

    # GET (load form html untuk modal)
    form = BeritaForm()
    html = render_to_string("news/berita_form.html", {"form": form}, request=request)
    return JsonResponse({"html": html})

def berita_edit(request, pk):
    item = get_object_or_404(Berita, pk=pk)

    if request.method == "POST":
        form = BeritaForm(request.POST, instance=item)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({
                "status": "ok",
                "id": obj.id,
                "url_detail": reverse('news:berita_detail', args=[obj.id]),
            })
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    # GET → return form sebagai HTML untuk modal
    form = BeritaForm(instance=item)
    html = render_to_string("news/berita_form.html", {"form": form}, request=request)
    return JsonResponse({"html": html})

def berita_delete(request, pk):
    item = get_object_or_404(Berita, pk=pk)
    if request.method == "POST":
        item.delete()
        return JsonResponse({"status":"ok"})
    return JsonResponse({"status":"error","msg":"invalid"}, status=405)
