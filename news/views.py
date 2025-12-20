from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BeritaForm
from .models import Berita
from following.views import getListOfNews, createSportOnStart
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.forms.models import model_to_dict
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

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

def berita_json_list(request):
    berita = Berita.objects.all().order_by('-id')

    data = []
    for item in berita:
        data.append({
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "category": item.category,
            "category_display": item.get_category_display(),
            "thumbnail": item.thumbnail,
            "author": item.author.username,
            "created_at" : item.created_at.isoformat(),
            "cabangOlahraga": item.cabangOlahraga.namaCabang if item.cabangOlahraga else None,
        })

    return JsonResponse(data, safe=False)

def berita_json_detail(request, pk):
    item = get_object_or_404(Berita, pk=pk)

    data = {
        "id": item.id,
        "title": item.title,
        "content": item.content,
        "category": item.category,
        "category_display": item.get_category_display(),
        "thumbnail": item.thumbnail,
        "author": item.author.username,
        "created_at" : item.created_at.isoformat(),
        "cabangOlahraga": item.cabangOlahraga.namaCabang if item.cabangOlahraga else None,
    }

    return JsonResponse(data)

@csrf_exempt
def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # --- TAMBAHAN PENTING: User-Agent ---
        # Kita pura-pura jadi Browser Chrome biasa
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Masukkan headers ke dalam request
        response = requests.get(image_url, headers=headers, timeout=10)
        
        # Cek apakah server gambar menolak (misal 403 Forbidden)
        response.raise_for_status()
        
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except Exception as e:
        # Print error di terminal Django biar ketahuan salahnya apa
        print(f"Error Proxy Image: {e}") 
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_news_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # === LOGIKA BARU UNTUK HANDLE USER ===
        if request.user.is_authenticated:
            # Kalau sudah login, pakai user yang login
            user = request.user
        else:
            # Kalau BELUM login, kita pinjam akun pertama di database (Admin)
            # Ini cuma buat ngetes biar ga error 500
            user = User.objects.first() 
        # ======================================

        title = strip_tags(data.get("title", ""))
        content = strip_tags(data.get("content", ""))
        category = data.get("category", "other")
        thumbnail = data.get("thumbnail", "")

        new_news = Berita(
            title=title, 
            content=content,
            category=category,
            thumbnail=thumbnail,
            author=user # Sekarang user pasti terisi (entah login atau pinjam admin)
        )
        new_news.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_flutter(request, pk):
    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "POST only"}, status=400)

    berita = get_object_or_404(Berita, pk=pk)
    berita.delete()
    return JsonResponse({"status": "success"})

@csrf_exempt
def edit_flutter(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Berita, pk=pk)
        data = json.loads(request.body)

        item.title = data.get("title", item.title)
        item.content = data.get("content", item.content)
        item.category = data.get("category", item.category)
        item.thumbnail = data.get("thumbnail", item.thumbnail)

        item.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=405)
