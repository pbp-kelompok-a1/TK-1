# ini utk file viewsnya profil_atlet/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Atlet
from .forms import AtletForm # import form 

# fungsi cek Admin 
# utk jadi Admin harus dipastikan punya status 'is_superuser' 
def is_admin(user):
    return user.is_superuser

# --- Bagian READ (Guest, Member, Admin) ---

# R (Read) - List Atlet
def list_atlet(request):
    # Admin bisa lihat semua, Guest & Member hanya lihat yg 'is_visible=True'
    if request.user.is_authenticated and request.user.is_superuser:
        atlet_list = Atlet.objects.all().order_by('name') # Admin lihat semua
    else:
        atlet_list = Atlet.objects.filter(is_visible=True).order_by('name') # lainnya lihat yg visible
        
    context = {'atlet_list': atlet_list}
    return render(request, 'profil_atlet/list_atlet.html', context)

# R (Read) - Detail Atlet
@login_required # hanya bisa diakses oleh yg LOGIN (Member) & Admin
def detail_atlet(request, pk):
    atlet = get_object_or_404(Atlet, pk=pk)
    
    # JIKA user BUKAN admin DAN atletnya di-set 'is_visible=False'
    # penjaga agar hanya Admin yang bisa melihat profil atlet yang sedang disembunyikan. 
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

# --- Bagian C-U-D (Hanya Admin) ---

# C (Create) - only Admin
@user_passes_test(is_admin) # decorator yang memanggil fungsi is_admin
def create_atlet(request):
    if request.method == 'POST':
        form = AtletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profil_atlet:list_atlet')
    else:
        form = AtletForm()
        
    context = {'form': form, 'page_title': 'Tambah Atlet Baru'}
    return render(request, 'profil_atlet/form_atlet.html', context)

# U (Update) - only Admin
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

# D (Delete) - only Admin
@user_passes_test(is_admin)
def delete_atlet(request, pk):
    atlet = get_object_or_404(Atlet, pk=pk)
    if request.method == 'POST':
        atlet.delete()
        return redirect('profil_atlet:list_atlet') 
        
    return render(request, 'profil_atlet/confirm_delete.html', {'atlet': atlet})