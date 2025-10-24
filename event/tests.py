from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta

from events.models import Event, EventType
from events.forms import EventForm
from following.models import CabangOlahraga


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass123")
        self.sport = CabangOlahraga.objects.create(namaCabang="Para Athletics")

    def test_event_str_and_type(self):
        """Test model string and event type property."""
        event = Event.objects.create(
            title="Test Event",
            description="Testing model",
            creator=self.user,
            cabangOlahraga=self.sport,
            start_time=timezone.now() + timedelta(days=1),
        )
        self.assertIn("Test Event", str(event))
        self.assertFalse(event.is_global_event)

    def test_global_event_property(self):
        event = Event.objects.create(
            title="Global Event",
            description="Admin event",
            creator=self.user,
            cabangOlahraga=self.sport,
            start_time=timezone.now() + timedelta(days=1),
            event_type=EventType.GLOBAL,
        )
        self.assertTrue(event.is_global_event)


class EventFormTest(TestCase):
    def setUp(self):
        self.sport = CabangOlahraga.objects.create(namaCabang="Para Athletics")

    def test_valid_form(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(days=1)
        form_data = {
            "title": "Valid Tournament",
            "description": "This is fine",
            "location": "Jakarta",
            "picture_url": "https://example.com/pic.jpg",
            "cabangOlahraga": self.sport.id,
            "start_time": start,
            "end_time": end,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_start_time_in_past_invalid(self):
        past = timezone.now() - timedelta(days=1)
        end = timezone.now() + timedelta(days=1)
        form_data = {
            "title": "Old Tournament",
            "description": "Invalid start time",
            "location": "Bandung",
            "picture_url": "https://example.com/old.jpg",
            "cabangOlahraga": self.sport.id,
            "start_time": past,
            "end_time": end,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Start time cannot be in the past.", str(form.errors))

    def test_end_time_before_start_invalid(self):
        start = timezone.now() + timedelta(days=2)
        end = timezone.now() + timedelta(days=1)
        form_data = {
            "title": "Invalid End Time",
            "description": "End time earlier than start",
            "location": "Surabaya",
            "picture_url": "https://example.com/end.jpg",
            "cabangOlahraga": self.sport.id,
            "start_time": start,
            "end_time": end,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("End time must be after start time.", str(form.errors))


class EventViewsTest(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="user", password="pass123")
        self.admin = User.objects.create_user(username="admin", password="pass123", is_staff=True)

        # Sport
        self.sport = CabangOlahraga.objects.create(namaCabang="Para Athletics")

        # Client
        self.client = Client()

        # URLs
        self.list_url = reverse("event:event_list")
        self.create_url = reverse("event:event_create")
        self.create_global_url = reverse("event:event_create_global")

        # Event sample
        self.event = Event.objects.create(
            title="Future Tournament",
            description="Sample event",
            location="Jakarta",
            picture_url="https://example.com/img.jpg",
            cabangOlahraga=self.sport,
            creator=self.user,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=2),
        )

    def test_event_list_status(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events_list.html")

    def test_event_list_contains_event(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, "Future Tournament")

    def test_create_requires_login(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_create_valid(self):
        self.client.login(username="user", password="pass123")
        start = (timezone.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        end = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")

        data = {
            "title": "Community Event",
            "description": "Fun event",
            "location": "Bali",
            "picture_url": "https://example.com/pic.jpg",
            "cabangOlahraga": self.sport.id,
            "start_time": start,
            "end_time": end,
        }
        response = self.client.post(self.create_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title="Community Event").exists())

    def test_create_global_non_admin_denied(self):
        self.client.login(username="user", password="pass123")
        response = self.client.get(self.create_global_url, follow=True)
        self.assertContains(response, "Only admins can create Global Events.")

    def test_create_global_admin_success(self):
        self.client.login(username="admin", password="pass123")
        start = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")
        end = (timezone.now() + timedelta(days=4)).strftime("%Y-%m-%dT%H:%M")

        data = {
            "title": "Global Event",
            "description": "Top tournament",
            "location": "Surabaya",
            "picture_url": "https://example.com/global.jpg",
            "cabangOlahraga": self.sport.id,
            "start_time": start,
            "end_time": end,
        }

        response = self.client.post(self.create_global_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(title="Global Event")
        self.assertEqual(event.event_type, EventType.GLOBAL)

    def test_delete_by_creator(self):
        self.client.login(username="user", password="pass123")
        delete_url = reverse("event:event_delete", args=[self.event.id])
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_delete_denied_for_others(self):
        other = User.objects.create_user(username="other", password="pass123")
        self.client.login(username="other", password="pass123")
        delete_url = reverse("event:event_delete", args=[self.event.id])
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, "Permission denied")
        self.assertTrue(Event.objects.filter(id=self.event.id).exists())

    def test_delete_admin_override(self):
        self.client.login(username="admin", password="pass123")
        delete_url = reverse("event:event_delete", args=[self.event.id])
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    # -------------------------------------------
    # AJAX delete
    # -------------------------------------------
    def test_ajax_delete_returns_json(self):
        self.client.login(username="user", password="pass123")
        event = Event.objects.create(
            title="AJAX Test",
            description="Ajax",
            creator=self.user,
            cabangOlahraga=self.sport,
            start_time=timezone.now() + timedelta(days=1),
        )
        delete_url = reverse("event:event_delete", args=[event.id])
        response = self.client.post(
            delete_url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": True, "message": f'Event "{event.title}" deleted successfully.'},
        )
