from django.db import models
from django.utils import timezone


# Create your models here.


class Prize(models.Model):
    prize_time = models.DateTimeField(default=timezone.now)
    img = models.FileField(max_length=255, upload_to='team/prize/')
    text = models.TextField(max_length=255, default='')
