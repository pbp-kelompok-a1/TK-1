from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

# Create your models here.
class CabangOlahraga(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, default="", editable=False)

class Following(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    priority = models.IntegerField(editable=True)

class EventType(models.TextChoices):
    GLOBAL = 'global', 'Global Tournament (Admin Only)'     # hanya bisa diupload oleh admin
    COMMUNITY = 'community', 'Community Tournament'         # bisa diupload oleh logged in user

class Event(models.Model): 
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    ) 
    
    title = models.CharField(max_length=200, verbose_name="Tournament Name")
    description = models.TextField(verbose_name="Description of the Tournament")
    
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Location / Venue (Optional)"
    )
    
    official_link = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Official Website Link (Recommended for Global Tournaments)"
    )
    
    start_time = models.DateTimeField(default=timezone.now, verbose_name="Start Time")

    event_type = models.CharField(
        max_length=10,
        choices=EventType.choices,
        default=EventType.COMMUNITY,
        verbose_name="Event Scope"
    )
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creator"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tournament Event"
        verbose_name_plural = "Tournament Events"
        ordering = ['start_time']

    # string helper buat nulis tanggal
    def __str__(self):
        return f"[{self.get_event_type_display()}] {self.title} @ {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    # buat cek jika global turnamen atau bukan
    @property
    def is_global_event(self):
        return self.event_type == EventType.GLOBAL