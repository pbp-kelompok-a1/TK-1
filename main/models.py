from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid
import os

# Create your models here.

class CustomUser(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, editable=False, related_name="customuser")
    join_date = models.DateTimeField(default=timezone.now, editable=False)
    username = models.CharField(max_length=100, editable=False)
    name = models.TextField(null=True, editable=True)
    picture = CloudinaryField('image', folder='paraworld/profiles', null=True, blank=True,
        transformation={
            'width': 500,
            'height': 500,
            'crop': 'limit',
            'quality': 'auto:good'
        }
    )
    picture_public_id = models.CharField(max_length=255, null=True, blank=True, editable=False)

    def __str__(self):
        return self.username
    
    def get_picture_url(self):
        if not self.picture:
            return None
            
        try:
            return self.picture.url
        except Exception as e:
            print(f"Error getting picture URL for {self.username}: {e}")
            return None