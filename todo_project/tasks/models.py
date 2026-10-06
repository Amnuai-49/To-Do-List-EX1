from django.conf import settings
from django.db import models

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    remind_at = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    reminded = models.BooleanField(default=False)  # กันส่งแจ้งเตือนซ้ำ
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["is_done", "remind_at", "-created_at"]
    def __str__(self): return self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=50, blank=True)
