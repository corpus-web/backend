from django.db import models
import os


class Course(models.Model):
    img = models.FileField(max_length=255, upload_to='course/')

    def delete(self, *args, **kwargs):
        # 删除文件
        if self.img:
            path = self.img.path
            if os.path.isfile(path):
                os.remove(path)

        # 调用父类的 delete() 方法
        super().delete(*args, **kwargs)
