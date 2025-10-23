# ini utk file viewsnya profil_atlet/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Atlet
from .forms import AtletForm # import form 
from django.db.models import Count, Q
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# fungsi cek Admin 
# utk jadi Admin harus dipastikan punya status 'is_superuser' 
def is_admin(user):
    return user.is_superuser

# Bagian READ (Guest, Member, Admin)

# R (Read) utk List Atlet
def list_atlet(request):
    # buat field 'medal_count'
    base_query = Atlet.objects.annotate(
        # count medali emas
        gold_count=Count('medali', filter=Q(medali__medal_type='Gold Medal')),
        # count medali perak
        silver_count=Count('medali', filter=Q(medali__medal_type='Silver Medal')),
        # count medali perunggu
        bronze_count=Count('medali', filter=Q(medali__medal_type='Bronze Medal')),
        # count total untuk cek (jika total = 0, kita hide)
        total_medals=Count('medali')
    )
    # Admin bisa lihat semua, Guest & Member hanya lihat yg 'is_visible=True'
    if request.user.is_authenticated and request.user.is_superuser:
        atlet_list = base_query.order_by('name') # Admin lihat semua
    else:
        atlet_list = base_query.filter(is_visible=True).order_by('name') # lainnya lihat yg visible
        
    context = {'atlet_list': atlet_list}
    return render(request, 'profil_atlet/list_atlet.html', context)

# R (Read) utk Detail Atlet
@login_required # decorator hanya bisa diakses oleh yg LOGIN (Member) & Admin
def detail_atlet(request, pk):
    atlet = get_object_or_404(Atlet, pk=pk)
    
    # JIKA user BUKAN admin DAN atletnya diset 'is_visible=False'
    # ini sbg penjaga agar hanya Admin yang bisa melihat profil atlet yang sedang disembunyikan. 
    # jika seorang Member (bukan admin) mencoba mengakses URL detail atlet yang disembunyikan, 
    # mereka akan ditolak dan dikembalikan ke halaman daftar.
    if not request.user.is_superuser and not atlet.is_visible:
        return redirect('profil_atlet:list_atlet') 
        
    # ambil juga data medali
    medali_list = atlet.medali.all()
        
    context = {
        'atlet': atlet,
        'medali_list': medali_list
    }
    return render(request, 'profil_atlet/detail_atlet.html', context)

# Bagian C-U-D (Hanya Admin)

# C (Create) only Admin
@user_passes_test(is_admin) # decorator yang memanggil fungsi is_admin
def create_atlet(request):
    if not request.user.is_superuser:
        return redirect('profil_atlet:list_atlet')
    
    form = AtletForm()
    context = {
        'form': form,
        'page_title': 'Tambah Atlet'
    }
    return render(request, 'profil_atlet/form_atlet.html', context)

# U (Update) only Admin
@user_passes_test(is_admin)
def update_atlet(request, pk):
    atlet = get_object_or_404(Atlet, pk=pk)
    if request.method == 'POST':
        form = AtletForm(request.POST, instance=atlet)
        if form.is_valid():
            form.save()
            return redirect('profil_atlet:detail_atlet', pk=atlet.pk) 
    else:
        form = AtletForm(instance=atlet)
        
    context = {'form': form, 'page_title': 'Edit Atlet'}
    return render(request, 'profil_atlet/form_atlet.html', context)

# D (Delete) only Admin
@user_passes_test(is_admin)
def delete_atlet(request, pk):
    atlet = get_object_or_404(Atlet, pk=pk)
    if request.method == 'POST':
        atlet.delete()
        return redirect('profil_atlet:list_atlet') 
        
    return render(request, 'profil_atlet/confirm_delete.html', {'atlet': atlet})

# function view utk  data JSON
def show_json_atlet(request):
    # kita ambil query yg sama persis dgnview list_atlet
    base_query = Atlet.objects.annotate(
        gold_count=Count('medali', filter=Q(medali__medal_type='Gold Medal')),
        silver_count=Count('medali', filter=Q(medali__medal_type='Silver Medal')),
        bronze_count=Count('medali', filter=Q(medali__medal_type='Bronze Medal')),
        total_medals=Count('medali')
    )

    if request.user.is_authenticated and request.user.is_superuser:
        atlet_list = base_query.order_by('name')
    else:
        atlet_list = base_query.filter(is_visible=True).order_by('name')
        
    data = []
    for atlet in atlet_list:
        data.append({
            'pk': atlet.pk,
            'name': atlet.name,
            'short_name': atlet.short_name,
            'discipline': atlet.discipline,
            'country': atlet.country,
            'is_visible': atlet.is_visible,
            'gold_count': atlet.gold_count,
            'silver_count': atlet.silver_count,
            'bronze_count': atlet.bronze_count,
            'total_medals': atlet.total_medals,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def create_atlet_ajax(request):
    if request.method == "POST":
        # tdk bisa pake request.POST biasa karena data dikirim sebagai JSON/FormData
        
        form = AtletForm(request.POST or None)

        if form.is_valid():
            form.save()
            # sinyal sukses
            return JsonResponse({"status": "success", "message": "Athlete added successfully!"}, status=201)
        else:
            # sinyal error beserta daftar error-nya
            return JsonResponse({"status": "error", "message": "Invalid form", "errors": form.errors}, status=400)

    # jika ada yg akses via GET, kirim error
    return JsonResponse({"status": "error", "message": "GET method is not allowed"}, status=405)

@csrf_exempt 
def delete_atlet_ajax(request, pk):
    if request.method == "DELETE":
        try:
            atlet = get_object_or_404(Atlet, pk=pk)
            atlet.delete()
            return JsonResponse({"status": "success", "message": "Athlete deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Method is not allowed"}, status=405)