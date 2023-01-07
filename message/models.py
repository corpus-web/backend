from django.db import models

from django.utils import timezone


class Message(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=32767)
    create_time = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=8)
