from django.db import models

from django.utils import timezone


class Meeting(models.Model):
    title = models.TextField(max_length=255)
    img = models.FileField(max_length=255, upload_to='academic/meeting/')
    abstract = models.TextField(max_length=255)
    text = models.TextField(max_length=32367)
    create_time = models.DateTimeField(default=timezone.now)
