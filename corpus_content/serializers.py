from rest_framework import serializers

from .models import ArticlePost, Picture

from config import addr


class ArticlePostSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    fileurl = serializers.SerializerMethodField()
    fid = serializers.SerializerMethodField()

    class Meta:
        model = ArticlePost
        fields = (
            "fid", "title", "author", "fileurl", "create_time"
        )

    def get_fid(self, obj):
        return obj.id

    def get_fileurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.file}"


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
