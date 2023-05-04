from django.db import models
from django.utils import timezone
import os


# Create your models here.


class Prize(models.Model):
    prize_time = models.DateTimeField(default=timezone.now)
    img = models.FileField(max_length=255, upload_to='team/prize/')
    text = models.TextField(max_length=255, default='')

    def delete(self, *args, **kwargs):
        # 删除文件
        if self.img:
            path = self.img.path
            if os.path.isfile(path):
                os.remove(path)

        # 调用父类的 delete() 方法
        super().delete(*args, **kwargs)
