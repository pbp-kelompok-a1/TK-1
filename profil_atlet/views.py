# ini utk file viewsnya profil_atlet/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Atlet, Medali
from .forms import AtletForm, MedaliForm # import form 
from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse
from following.models import CabangOlahraga

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
        atlet_list = base_query.filter(is_visible=True).order_by(Lower('name')) # lainnya lihat yg visible
        
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
        'page_title': 'Tambah Atlet',
        'back_url': reverse('profil_atlet:list_atlet')
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
        
    context = {'form': form, 'page_title': 'Edit Atlet', 'back_url': reverse('profil_atlet:detail_atlet', args=[atlet.pk])}
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
    base_query = Atlet.objects.select_related('discipline').annotate(
        gold_count=Count('medali', filter=Q(medali__medal_type='Gold Medal')),
        silver_count=Count('medali', filter=Q(medali__medal_type='Silver Medal')),
        bronze_count=Count('medali', filter=Q(medali__medal_type='Bronze Medal')),
        total_medals=Count('medali')
    )

    if request.user.is_authenticated and request.user.is_superuser:
        atlet_list = base_query.order_by('discipline__name', Lower('name'))
    else:
        atlet_list = base_query.filter(is_visible=True).order_by(Lower('name'))
        
    data = []
    for atlet in atlet_list:
        nama_discipline = atlet.discipline.name if atlet.discipline else "General"
        data.append({
            'pk': atlet.pk,
            'name': atlet.name,
            'short_name': atlet.short_name or "-", 
            'discipline': nama_discipline,
            'country': atlet.country,
            'is_visible': atlet.is_visible,
            'gold_count': atlet.gold_count,
            'silver_count': atlet.silver_count,
            'bronze_count': atlet.bronze_count,
            'total_medals': atlet.total_medals,
            # Tambahan fields biar form Flutter gak kosong
            'gender': atlet.gender,
            'birth_date': str(atlet.birth_date) if atlet.birth_date else "",
            'birth_place': atlet.birth_place,
            'birth_country': atlet.birth_country,
            'nationality': atlet.nationality,
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
    if request.method == "POST" or request.method == "DELETE":
        try:
            atlet = get_object_or_404(Atlet, pk=pk)
            atlet.delete()
            return JsonResponse({"status": "success", "message": "Athlete deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Method is not allowed"}, status=405)

# C (Create) untuk Medali
@user_passes_test(is_admin)
def create_medali(request, atlet_pk):
    atlet = get_object_or_404(Atlet, pk=atlet_pk)
    
    if request.method == 'POST':
        form = MedaliForm(request.POST)
        if form.is_valid():
            medali = form.save(commit=False)
            medali.atlet = atlet
            medali.save()
            return redirect('profil_atlet:detail_atlet', pk=atlet_pk)
    else:
        form = MedaliForm()

    context = {
        'form': form, 
        'atlet': atlet, 
        'page_title': 'Add Medal',
        'back_url': reverse('profil_atlet:detail_atlet', args=[atlet_pk])
    }
    return render(request, 'profil_atlet/form_atlet.html', context)

# U (Update) untuk Medali
@user_passes_test(is_admin)
def update_medali(request, medal_pk):
    medali = get_object_or_404(Medali, pk=medal_pk)
    
    if request.method == 'POST':
        form = MedaliForm(request.POST, instance=medali)
        if form.is_valid():
            form.save()
            return redirect('profil_atlet:detail_atlet', pk=medali.atlet.pk)
    else:
        form = MedaliForm(instance=medali)

    context = {
        'form': form, 
        'atlet': medali.atlet, 
        'page_title': 'Edit Medal',
        'back_url': reverse('profil_atlet:detail_atlet', args=[medali.atlet.pk])
    }
    return render(request, 'profil_atlet/form_atlet.html', context)

# D (Delete) untuk Medali
@user_passes_test(is_admin)
def delete_medali(request, medal_pk):
    medali = get_object_or_404(Medali, pk=medal_pk)
    atlet_pk = medali.atlet.pk # Simpan PK atlet sebelum dihapus
    
    if request.method == 'POST':
        medali.delete()
        return redirect('profil_atlet:detail_atlet', pk=atlet_pk)
    
    # Kita akalin 'confirm_delete.html' biar generik
    context = {
        'object': medali,
       'object_name': f"Medal: {medali.event} ({medali.medal_date})",
        'back_url': reverse('profil_atlet:detail_atlet', args=[atlet_pk])
    }
    return render(request, 'profil_atlet/confirm_delete.html', context)

def show_json_detail_atlet(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    atlet = get_object_or_404(Atlet, pk=pk)
    
    # ambil data medali terkait
    medali_data = []
    for m in atlet.medali.all():
        medali_data.append({
            'pk': m.pk,
            'medal_type': m.medal_type,
            'event': m.event,
            'medal_date': m.medal_date
        })

    data = {
        'pk': atlet.pk,
        'name': atlet.name,
        'short_name': atlet.short_name or "-",
        'country': atlet.country,
        'discipline': atlet.discipline.name if atlet.discipline else "General",
        'birth_date': str(atlet.birth_date) if atlet.birth_date else None,
        'gender': atlet.gender,
        'nationality': atlet.nationality or "-",
        'birth_place': atlet.birth_place,
        'birth_country': atlet.birth_country,
        'medali_list': medali_data,
    }
    return JsonResponse(data)

@csrf_exempt
def edit_atlet_flutter(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    if request.method == 'POST':
        try:
            atlet = Atlet.objects.get(pk=pk)
            data = json.loads(request.body)
            atlet.name = data.get('name', atlet.name)
            atlet.short_name = data.get('short_name', atlet.short_name)
            atlet.country = data.get('country', atlet.country)
            atlet.gender = data.get('gender', atlet.gender)
            atlet.birth_place = data.get('birth_place', atlet.birth_place)
            atlet.birth_country = data.get('birth_country', atlet.birth_country)
            atlet.nationality = data.get('nationality', atlet.nationality)
            
            birth_date = data.get('birth_date')
            if birth_date and birth_date.strip() != "":
                atlet.birth_date = birth_date

            discipline_name = data.get('discipline')
            if discipline_name:
                cabor_obj, _ = CabangOlahraga.objects.get_or_create(name=discipline_name)
                atlet.discipline = cabor_obj

            atlet.save()
            return JsonResponse({"status": "success", "message": "Athlete updated!"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def create_atlet_flutter(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            discipline_name = data.get('discipline', 'General')
            cabor_obj, _ = CabangOlahraga.objects.get_or_create(name=discipline_name)

            # Buat atlet dengan data lengkap
            new_atlet = Atlet.objects.create(
                name=data.get('name'),
                short_name=data.get('short_name'),
                country=data.get('country'),
                discipline=cabor_obj,
                gender=data.get('gender'),
                birth_place=data.get('birth_place'),
                birth_country=data.get('birth_country'),
                nationality=data.get('nationality'),
                is_visible=True, 
            )

            # Handling date
            birth_date_str = data.get('birth_date')
            if birth_date_str and birth_date_str.strip() != "":
                new_atlet.birth_date = birth_date_str
                new_atlet.save()

            return JsonResponse({"status": "success", "message": "New athlete created successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def edit_medali_flutter(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    if request.method == 'POST':
        try:
            medali = Medali.objects.get(pk=pk)
            data = json.loads(request.body)
            
            # Update field medali
            medali.medal_type = data.get('medal_type', medali.medal_type)
            medali.event = data.get('event', medali.event)
            medali.medal_date = data.get('medal_date', medali.medal_date)
            
            medali.save()
            return JsonResponse({"status": "success", "message": "Medal updated!"}, status=200)
        except Medali.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Medal not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def delete_medali_flutter(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    if request.method == "POST":
        try:
            medali = Medali.objects.get(pk=pk)
            medali.delete()
            return JsonResponse({"status": "success", "message": "Medal deleted"}, status=200)
        except Medali.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Medal not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def add_medali_flutter(request, atlet_pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    if request.method == 'POST':
        try:
            atlet = Atlet.objects.get(pk=atlet_pk)
            data = json.loads(request.body)
            
            # Ambil data medali, pastikan medal_type sesuai (Gold Medal, Silver Medal, Bronze Medal)
            Medali.objects.create(
                atlet=atlet,
                medal_type=data.get('medal_type'), # User harus input lengkap atau pake dropdown di Flutter
                event=data.get('event'),
                medal_date=data.get('medal_date') 
            )
            return JsonResponse({"status": "success", "message": "Medal added!"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)