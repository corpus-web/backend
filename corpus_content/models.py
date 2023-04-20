from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)


class File(models.Model):
    name = models.CharField(max_length=255, default="noname")
    sub_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    text = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)


class Picture(models.Model):
    img = models.FileField(max_length=255, upload_to='corpus/img/')
