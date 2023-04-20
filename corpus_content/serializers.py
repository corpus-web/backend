from rest_framework import serializers

# from .models import ArticlePost
from .models import Picture, Category, File

from config import addr


class PictureSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()
    pid = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = (
            'pictureurl', 'pid'
        )

    def get_pictureurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.img}"

    def get_pid(self, obj):
        return obj.id


class CategorySerializer(serializers.ModelSerializer):
    cid = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'cid', 'name', 'name_en'
        )

    def get_cid(self, obj):
        return obj.id


class FileSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    fid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = File
        fields = (
            'fid', 'name', 'sub_name', 'category', 'create_time'
        )

    def get_fid(self, obj):
        return obj.id
