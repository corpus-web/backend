from django.db import models


class Course(models.Model):
    img = models.FileField(max_length=255, upload_to='course/')
