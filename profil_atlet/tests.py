from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Atlet 

# NGETES SEBAGAI GUEST (TIDAK LOGIN)
class AtletGuestTests(TestCase):
    def setUp(self):
        self.client = Client()
        Atlet.objects.create(name="Atlet Visible", discipline="Discipline", country="Country", gender="Male", is_visible=True)
        Atlet.objects.create(name="Atlet Hidden", discipline="Discipline", country="Country", gender="Male", is_visible=False)
    
    def test_json_endpoint_for_guest(self):
        response = self.client.get(reverse('profil_atlet:show_json_atlet'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Atlet Visible")

    def test_guest_cannot_access_detail_page(self):
        atlet = Atlet.objects.get(name="Atlet Visible")
        response = self.client.get(reverse('profil_atlet:detail_atlet', args=[atlet.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/atlet/{atlet.pk}/')

    def test_guest_cannot_access_create_page(self):
        response = self.client.get(reverse('profil_atlet:create_atlet'))
        self.assertEqual(response.status_code, 302)
        
    def test_guest_cannot_access_update_page(self):
        atlet = Atlet.objects.get(name="Atlet Visible")
        response = self.client.get(reverse('profil_atlet:update_atlet', args=[atlet.pk]))
        self.assertEqual(response.status_code, 302)

# NGETES SEBAGAI MEMBER (LOGIN, TAPI NOT ADMIN)
class AtletRegularUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.regular_user = User.objects.create_user('member', 'member@example.com', 'memberpass')
        cls.atlet_visible = Atlet.objects.create(name="Atlet Visible", discipline="Discipline", country="Country", gender="Male", is_visible=True)
        cls.atlet_hidden = Atlet.objects.create(name="Atlet Hidden", discipline="Discipline", country="Country", gender="Male", is_visible=False)

    def setUp(self):
        self.client = Client()
        self.client.login(username='member', password='memberpass')

    def test_regular_user_can_see_VISIBLE_atlet_detail(self):
        response = self.client.get(reverse('profil_atlet:detail_atlet', args=[self.atlet_visible.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atlet Visible")

    def test_regular_user_CANNOT_see_HIDDEN_atlet_detail(self):
        response = self.client.get(reverse('profil_atlet:detail_atlet', args=[self.atlet_hidden.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profil_atlet:list_atlet'))

# NGETES SEBAGAI ADMIN (SUPERUSER)
class AtletAdminTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser('admin_views', 'admin@example.com', 'adminpass')
        cls.atlet1 = Atlet.objects.create(name="Atlet A", discipline="Discipline", country="Country", gender="Male", is_visible=True)
        cls.atlet_buat_dihapus = Atlet.objects.create(name="Test Atlet for Delete", discipline="Testing", country="Testland", gender="Male")

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin_views', password='adminpass')

    def test_admin_sees_all_json(self):
        Atlet.objects.create(name="Atlet Hidden", discipline="Discipline", country="Country", gender="Male", is_visible=False)
        response = self.client.get(reverse('profil_atlet:show_json_atlet'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)

    def test_admin_can_access_create_page(self):
        response = self.client.get(reverse('profil_atlet:create_atlet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profil_atlet/form_atlet.html')

    def test_update_view_get_and_post(self):
        atlet_pk = self.atlet1.pk
        
        response_get = self.client.get(reverse('profil_atlet:update_atlet', args=[atlet_pk]))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'profil_atlet/form_atlet.html')

        response_post = self.client.post(reverse('profil_atlet:update_atlet', args=[atlet_pk]), {
            'name': 'Atlet A Updated',
            'discipline': 'Discipline',
            'country': 'Country',
            'gender': 'Male',
            'birth_date': '01/01/2001'
        })
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse('profil_atlet:detail_atlet', args=[atlet_pk]))
        
        self.atlet1.refresh_from_db()
        self.assertEqual(self.atlet1.name, "Atlet A Updated")

    def test_delete_view_get_and_post(self):
        atlet_pk = self.atlet1.pk

        response_get = self.client.get(reverse('profil_atlet:delete_atlet', args=[atlet_pk]))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'profil_atlet/confirm_delete.html')

        self.assertTrue(Atlet.objects.filter(pk=atlet_pk).exists())
        response_post = self.client.post(reverse('profil_atlet:delete_atlet', args=[atlet_pk]))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse('profil_atlet:list_atlet'))
        self.assertFalse(Atlet.objects.filter(pk=atlet_pk).exists())

    def test_create_atlet_ajax_happy_path_all_fields(self):
        response = self.client.post(reverse('profil_atlet:create_atlet_ajax'), {
            'name': '<p>Atlet Baru</p>',
            'short_name': 'AB',
            'discipline': 'Unit Test',
            'country': 'Testland',
            'gender': 'Female',
            'birth_date': '01/01/2001',
            'birth_place': 'Test City',
            'birth_country': 'Testland',
            'nationality': 'Testland'
        })
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        
        new_atlet = Atlet.objects.get(short_name='AB')
        self.assertEqual(new_atlet.name, "Atlet Baru")

    def test_create_atlet_ajax_form_invalid_sad_path(self):
        response = self.client.post(reverse('profil_atlet:create_atlet_ajax'), {
            'name': 'Atlet Gagal',
        })
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('discipline', data['errors'])
        self.assertFalse(Atlet.objects.filter(name='Atlet Gagal').exists())

    def test_delete_atlet_ajax_logic_works(self):
        atlet_pk = self.atlet_buat_dihapus.pk
        response = self.client.delete(reverse('profil_atlet:delete_atlet_ajax', args=[atlet_pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_create_atlet_ajax_wrong_method(self):
        response = self.client.get(reverse('profil_atlet:create_atlet_ajax'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['status'], 'error')

    def test_delete_atlet_ajax_wrong_method(self):
        atlet_pk = self.atlet_buat_dihapus.pk
        response = self.client.post(reverse('profil_atlet:delete_atlet_ajax', args=[atlet_pk]))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['status'], 'error')

    def test_delete_atlet_ajax_not_found(self):
        response = self.client.delete(reverse('profil_atlet:delete_atlet_ajax', args=[9999]))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['status'], 'error')