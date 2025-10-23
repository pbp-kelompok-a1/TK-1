from django.db import models
from django.contrib.auth.models import User

from following.models import CabangOlahraga

class Berita(models.Model):

    CATEGORY_CHOICES = [
        ('athlete', 'Athlete Story'),
        ('event', 'Event'),
        ('medal', 'Medal Result'),
        ('inspiration', 'Inspiration'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    thumbnail = models.URLField(blank=True, null=True)
    cabangOlahraga = models.ForeignKey(CabangOlahraga, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:60]
