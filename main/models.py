from django.db import models
import uuid

# Create your models here.
class CabangOlahraga(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, default="", editable=False)

class Following(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    priority = models.IntegerField(editable=True)