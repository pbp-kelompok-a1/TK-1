from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

from following.models import CabangOlahraga

User = settings.AUTH_USER_MODEL

class EventType(models.TextChoices):
    GLOBAL = 'global', 'Global Tournament (Admin Only)' 
    COMMUNITY = 'community', 'Community Tournament'

# Choices for Cabang Olahraga
class SportBranch(models.TextChoices):
    TENNIS = 'tennis', 'Tennis'
    SWIMMING = 'swim', 'Swimming'
    ATHLETICS = 'ath', 'Athletics'
    BASKETBALL = 'basket', 'Wheelchair Basketball'
    OTHER = 'other', 'Other'

class Event(models.Model): 
    # Primary Key
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    ) 
    
    # Core Event Details
    title = models.CharField(max_length=200, verbose_name="Tournament Name")
    description = models.TextField(verbose_name="Description of the Tournament")
    
    # Sport Branch
    sport_branch = models.CharField(
        max_length=10,
        choices=SportBranch.choices,
        default=SportBranch.OTHER,
        verbose_name="Cabang Olahraga"
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Location / Venue (Optional)"
    )
    
    # Visual Fields
    picture_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Tournament Image URL"
    )
    end_time = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Time Ends (Optional)"
    )

    # Scheduling
    start_time = models.DateTimeField(default=timezone.now, verbose_name="Start Time")

    # Event Type and Creator
    event_type = models.CharField(
        max_length=10,
        choices=EventType.choices,
        default=EventType.COMMUNITY,
        verbose_name="Event Scope"
    )
    
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events',
        verbose_name="Creator"
    )

    cabangOlahraga = models.ForeignKey(CabangOlahraga, default=None, on_delete=models.CASCADE, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tournament Event"
        verbose_name_plural = "Tournament Events"
        ordering = ['start_time']

    def __str__(self):
        return f"[{self.get_event_type_display()}] {self.title} - {self.get_sport_branch_display()}"

    @property
    def is_global_event(self):
        return self.event_type == EventType.GLOBAL