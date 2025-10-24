from django.test import TestCase, Client
from django.urls import reverse
from uuid import uuid4
from django.contrib.auth.models import User
from .models import CabangOlahraga, Following
from .forms import FollowingForm, OlahragaForm

# Create your tests here. 
class CabangOlahragaModelTest(TestCase):
    def testCreate(self):
        sport = CabangOlahraga.objects.create(name="Football")
        self.assertEqual(str(sport), "Football")
        self.assertIsInstance(sport.id, uuid4().__class__)

class FollowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='testpass')
        self.sport = CabangOlahraga.objects.create(name="Basketball")

    def testCreate(self):
        following = Following.objects.create(user=self.user, cabangOlahraga=self.sport)
        self.assertEqual(following.user.username, 'john')
        self.assertEqual(following.cabangOlahraga.name, 'Basketball')
        self.assertIsInstance(following.id, uuid4().__class__)


class OlahragaFormTest(TestCase):
    def testValid(self):
        form_data = {'name': 'Badminton'}
        form = OlahragaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testInvalid(self):
        form_data = {'name': ''} 
        form = OlahragaForm(data=form_data)
        self.assertFalse(form.is_valid())


class FollowingFormTest(TestCase):
    def setUp(self):
        self.sport = CabangOlahraga.objects.create(name="Tennis")

    def testValid(self):
        form = FollowingForm(data={'cabangOlahraga': self.sport.id})
        self.assertTrue(form.is_valid())

    def testInvalid(self):
        form = FollowingForm(data={})
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='password123')
        self.sport = CabangOlahraga.objects.create(name="Volleyball")
        self.following = Following.objects.create(user=self.user, cabangOlahraga=self.sport)

    def testProfilePage(self):
        self.client.login(username='alice', password='password123')
        response = self.client.get(reverse('profile', kwargs={'userId': self.user.id}))
        self.assertIn(response.status_code, [200, 302]) 

    def testCreateCabangOlahraga(self):
        admin = User.objects.create_superuser(username='root', password='toor', email='root@test.com')
        self.client.login(username='root', password='toor')
        response = self.client.post(reverse('createSport'), {'name': 'Swimming'})
        self.assertTrue(CabangOlahraga.objects.filter(name='Swimming').exists())