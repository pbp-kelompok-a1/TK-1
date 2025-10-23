from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, editable=False)
    username = models.CharField(max_length=100, editable=False)
    name = models.TextField(editable=True)
    picture = models.ImageField(null=True, editable=True)

    def __str__(self):
        return self.username