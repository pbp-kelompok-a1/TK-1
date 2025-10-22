from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Berita

class BeritaTestCase(TestCase):
    def setUp(self):
        # bikin user admin
        self.admin = User.objects.create_user(username='admin', password='12345', is_staff=True)

        # login admin
        self.client = Client()
        self.client.login(username='admin', password='12345')

        # buat 1 berita dummy
        self.berita = Berita.objects.create(
            title="Test News",
            content="This is test content",
            category="other",
            author=self.admin
        )

    def test_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get('/berita/')
        self.assertEqual(response.status_code, 302)  # redirect ke login

    def test_list_view_logged_in(self):
        response = self.client.get('/berita/')
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        response = self.client.get(f'/berita/{self.berita.id}/')
        self.assertEqual(response.status_code, 200)

    def test_only_staff_can_add(self):
        self.client.logout()
        normal_user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')

        response = self.client.get('/berita/add/')
        self.assertEqual(response.status_code, 403)  # forbidden

    def test_owner_can_edit(self):
        response = self.client.get(f'/berita/{self.berita.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_edit(self):
        other = User.objects.create_user(username='other', password='12345', is_staff=True)
        self.client.logout()
        self.client.login(username='other', password='12345')

        response = self.client.get(f'/berita/{self.berita.id}/edit/')
        self.assertEqual(response.status_code, 403)  # forbidden

    def test_create_news_post(self):
        # hanya staff/admin bisa add
        response = self.client.post('/berita/add/', {
            'title': 'New Title',
            'content': 'Some content',
            'category': 'other',
            'thumbnail': 'http://example.com/img.jpg'
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertEqual(Berita.objects.count(), 2)  # bertambah 1

    def test_delete_owner(self):
        response = self.client.post(f'/berita/{self.berita.id}/delete/')
        self.assertEqual(response.status_code, 302)  # redirect to list
        self.assertEqual(Berita.objects.count(), 0)

    def test_delete_not_owner(self):
        other = User.objects.create_user(username='other', password='12345', is_staff=True)
        self.client.logout()
        self.client.login(username='other', password='12345')
        response = self.client.post(f'/berita/{self.berita.id}/delete/')
        self.assertEqual(response.status_code, 403)  # forbidden
        self.assertEqual(Berita.objects.count(), 1)

    def test_form_valid(self):
        from .forms import BeritaForm
        form = BeritaForm(data={
            'title': 'Tes',
            'content': 'Isi',
            'category': 'other',
            'thumbnail': ''
        })
        self.assertTrue(form.is_valid())
