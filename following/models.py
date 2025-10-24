from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class CabangOlahraga(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, default="", editable=True)

class Following(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cabangOlahraga = models.ForeignKey(CabangOlahraga, on_delete=models.CASCADE, null=True)
    priority = models.IntegerField(editable=True)