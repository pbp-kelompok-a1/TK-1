# news/tests.py
import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch # Penting untuk mocking

# Import model dari modul Anda dan modul 'following'
from .models import Berita
from .forms import BeritaForm
from following.models import CabangOlahraga 

# CATATAN: Ganti 'following.models' jika nama app-nya berbeda

class BeritaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Buat objek-objek yang dibutuhkan sekali saja untuk semua tes di kelas ini
        cls.user = User.objects.create_user(username='testuser', password='password123')
        # GANTI: 'nama' -> 'name'
        cls.cabor = CabangOlahraga.objects.create(name='Sepak Bola') 
        cls.berita = Berita.objects.create(
            title="Judul Berita Pertama",
            content="Ini adalah isi konten berita.",
            category="event",
            author=cls.user,
            cabangOlahraga=cls.cabor
        )

    def test_berita_creation(self):
        # Tes apakah objek berhasil dibuat di setUpTestData
        self.assertEqual(self.berita.title, "Judul Berita Pertama")
        self.assertEqual(self.berita.author.username, 'testuser')
        # GANTI: 'nama' -> 'name'
        self.assertEqual(self.berita.cabangOlahraga.name, 'Sepak Bola')
        self.assertEqual(self.berita.category, 'event')

    def test_berita_str_method(self):
        # Tes metode __str__
        expected_str = self.berita.title[:60]
        self.assertEqual(str(self.berita), expected_str)

    def test_berita_category_default(self):
        # Tes nilai default 'category'
        default_berita = Berita.objects.create(
            title="Judul Default",
            content="Isi default.",
            author=self.user
        )
        self.assertEqual(default_berita.category, 'other')


class BeritaFormTest(TestCase):

    def test_berita_form_valid(self):
        # Tes form dengan data valid
        data = {
            'title': 'Judul Valid',
            'content': 'Konten yang valid.',
            'category': 'athlete',
            'thumbnail': 'https://google.com/image.png'
        }
        form = BeritaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_berita_form_invalid_no_title(self):
        # Tes form tanpa 'title' (required)
        data = {
            'content': 'Konten tanpa judul.',
            'category': 'athlete',
        }
        form = BeritaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_berita_form_invalid_no_content(self):
        # Tes form tanpa 'content' (required)
        data = {
            'title': 'Judul tanpa konten',
            'category': 'athlete',
        }
        form = BeritaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_berita_form_invalid_category(self):
        # Tes form dengan 'category' yang tidak valid
        data = {
            'title': 'Judul Valid',
            'content': 'Konten valid.',
            'category': 'kategori_salah', # Ini tidak ada di CHOICES
        }
        form = BeritaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_berita_form_thumbnail_optional(self):
        # Tes 'thumbnail' bersifat opsional
        data = {
            'title': 'Judul Valid',
            'content': 'Konten yang valid.',
            'category': 'athlete',
            # Tidak ada thumbnail
        }
        form = BeritaForm(data=data)
        self.assertTrue(form.is_valid())


class BeritaViewsTest(TestCase):

    def setUp(self):
        # setUp berjalan untuk SETIAP fungsi tes
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        # GANTI: 'nama' -> 'name'
        self.cabor = CabangOlahraga.objects.create(name='Badminton')
        self.berita1 = Berita.objects.create(
            title="Berita Badminton",
            content="Konten badminton.",
            category="event",
            author=self.user,
            cabangOlahraga=self.cabor
        )
        self.berita2 = Berita.objects.create(
            title="Berita Lain",
            content="Konten lain.",
            category="other",
            author=self.user
        )

        # Definisikan URL
        self.list_url = reverse('news:berita_list')
        self.add_url = reverse('news:berita_add')
        self.detail_url = reverse('news:berita_detail', args=[self.berita1.pk])
        self.edit_url = reverse('news:berita_edit', args=[self.berita1.pk])
        self.delete_url = reverse('news:berita_delete', args=[self.berita1.pk])
        self.invalid_detail_url = reverse('news:berita_detail', args=[999])
        self.invalid_edit_url = reverse('news:berita_edit', args=[999])
        self.invalid_delete_url = reverse('news:berita_delete', args=[999])

    # --- Tes berita_list ---

    # Kita 'patch' (mock) fungsi eksternal agar tes ini FOKUS pada logika view 'berita_list'
    @patch('news.views.createSportOnStart2') 
    @patch('news.views.getListOfNews', side_effect=Exception("Mocked error"))
    def test_berita_list_view_anonymous(self, mock_getListOfNews, mock_createSportOnStart2):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200) # Pastikan view tidak crash
        self.assertTemplateUsed(response, 'news/berita_list.html')
        mock_createSportOnStart2.assert_called_once() # Pastikan fungsi ini dipanggil
        
        # UBAH ASSERTION INI:
        # Karena view-nya SELALU memanggil getListOfNews, kita pastikan itu dipanggil
        mock_getListOfNews.assert_called_once() 

        # Karena mock-nya melempar error, view akan masuk ke blok 'except'
        # dan menggunakan fallback (semua berita).
        self.assertContains(response, self.berita1.title)
        self.assertContains(response, self.berita2.title)

    @patch('news.views.createSportOnStart2')
    @patch('news.views.getListOfNews')
    def test_berita_list_view_logged_in(self, mock_getListOfNews, mock_createSportOnStart2):
        # Simulasikan 'getListOfNews' mengembalikan hanya berita1
        mock_getListOfNews.return_value = Berita.objects.filter(pk=self.berita1.pk)
        
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        mock_createSportOnStart2.assert_called_once()
        mock_getListOfNews.assert_called_once_with(self.user) # Dipanggil dengan user yg login
        # Cek bahwa HANYA berita1 yang ada (sesuai mock)
        self.assertContains(response, self.berita1.title)
        self.assertNotContains(response, self.berita2.title)

    @patch('news.views.createSportOnStart2')
    @patch('news.views.getListOfNews', side_effect=Exception("Test Error")) # Simulasikan error
    def test_berita_list_view_getNews_fails(self, mock_getListOfNews, mock_createSportOnStart2):
        # Tes blok try...except
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200) # View tetap sukses (tidak crash)
        mock_createSportOnStart2.assert_called_once()
        mock_getListOfNews.assert_called_once_with(self.user)
        # Cek bahwa fallback (semua berita) digunakan
        self.assertContains(response, self.berita1.title)
        self.assertContains(response, self.berita2.title)

    # --- Tes berita_detail ---

    def test_berita_detail_view_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/berita_detail.html')
        self.assertEqual(response.context['b'], self.berita1) # Pastikan objek yg benar di pass

    def test_berita_detail_view_not_found(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, 404)

    # --- Tes berita_create ---

    def test_berita_create_get_anonymous(self):
        response = self.client.get(self.add_url)
        # @login_required akan redirect ke login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_berita_create_get_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.add_url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('html', data) # Cek respons JSON berisi HTML form

    def test_berita_create_post_success(self):
        self.client.login(username='testuser', password='password123')
        post_data = {
            'title': 'Berita Baru via Test',
            'content': 'Konten baru.',
            'category': 'inspiration',
            'thumbnail': 'https://google.com/img.jpg'
        }
        # Hitung jumlah berita sebelum POST
        count_before = Berita.objects.count()
        response = self.client.post(self.add_url, post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Berita.objects.count(), count_before + 1)
        
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['title'], 'Berita Baru via Test')
        
        # Cek apakah author diset dengan benar
        new_berita = Berita.objects.get(pk=data['id'])
        self.assertEqual(new_berita.author, self.user)

    def test_berita_create_post_invalid(self):
        self.client.login(username='testuser', password='password123')
        post_data = {
            'title': 'Judul ada',
            # 'content' (required) hilang
        }
        count_before = Berita.objects.count()
        response = self.client.post(self.add_url, post_data)

        self.assertEqual(response.status_code, 400) # Status 400 Bad Request
        self.assertEqual(Berita.objects.count(), count_before) # Tidak ada berita baru dibuat
        
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('content', data['errors']) # Cek 'content' ada di list error

    # --- Tes berita_edit ---
    
    # PERHATIAN: View 'berita_edit' Anda tidak memiliki @login_required.
    # Tes ini ditulis sesuai kode Anda. Jika ini bug, tes akan gagal saat Anda menambah @login_required.
    
    def test_berita_edit_get_success(self):
        # Saat ini tidak perlu login sesuai kode
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('html', data)
        self.assertIn(self.berita1.title, data['html']) # Pastikan form diisi data lama

    def test_berita_edit_get_not_found(self):
        response = self.client.get(self.invalid_edit_url)
        self.assertEqual(response.status_code, 404)

    def test_berita_edit_post_success(self):
        post_data = {
            'title': 'Judul Telah Diupdate',
            'content': self.berita1.content, # Kirim data lengkap
            'category': self.berita1.category,
            'thumbnail': self.berita1.thumbnail or ''
        }
        response = self.client.post(self.edit_url, post_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        
        # Cek database
        self.berita1.refresh_from_db()
        self.assertEqual(self.berita1.title, 'Judul Telah Diupdate')

    def test_berita_edit_post_invalid(self):
        post_data = {
            'title': '', # Judul dikosongkan (invalid)
            'content': 'Konten tetap ada.',
            'category': 'event',
        }
        response = self.client.post(self.edit_url, post_data)
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('title', data['errors'])

    # --- Tes berita_delete ---

    # PERHATIAN: View 'berita_delete' Anda tidak memiliki @login_required
    # atau pengecekan 'author'. Ini berisiko.
    
    def test_berita_delete_get_method_not_allowed(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 405) # 405 Method Not Allowed
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_berita_delete_post_success(self):
        count_before = Berita.objects.count()
        response = self.client.post(self.delete_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Berita.objects.count(), count_before - 1)
        
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        
        # Pastikan objeknya benar-benar hilang
        with self.assertRaises(Berita.DoesNotExist):
            Berita.objects.get(pk=self.berita1.pk)

    def test_berita_delete_post_not_found(self):
        response = self.client.post(self.invalid_delete_url)
        self.assertEqual(response.status_code, 404)