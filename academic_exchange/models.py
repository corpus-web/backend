from django.db import models

from django.utils import timezone
import os


class Meeting(models.Model):
    title = models.TextField(max_length=255)
    img = models.FileField(max_length=255, upload_to='academic/meeting/')
    abstract = models.TextField(max_length=255)
    text = models.TextField(max_length=32367)
    create_time = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):
        # 删除文件
        if self.img:
            path = self.img.path
            if os.path.isfile(path):
                os.remove(path)

        # 调用父类的 delete() 方法
        super().delete(*args, **kwargs)
