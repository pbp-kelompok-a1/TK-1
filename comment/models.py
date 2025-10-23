from django.db import models
from django.contrib.auth.models import User
from news.models import Berita  # pastikan app news punya model News

class Comment(models.Model):
    news = models.ForeignKey('news.Berita', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField("Comment", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.content[:40]}"

    class Meta:
        ordering = ['-created_at']
