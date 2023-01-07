from django.db import models


# Create your models here.


class Home(models.Model):
    img = models.FileField(max_length=255, upload_to='home/')
