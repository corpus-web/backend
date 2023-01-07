from rest_framework import serializers

from .models import Meeting

from config import addr


class MeetingTitleSerializer(serializers.ModelSerializer):
    aid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Meeting
        fields = (
            "title", "aid", "create_time"
        )

    def get_aid(self, obj):
        return obj.id


class MeetingContentSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()
    text_par = serializers.SerializerMethodField()
    aid = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            "title", "aid", "pictureurl", "abstract", "text_par",
        )

    def get_pictureurl(self, obj):
        return [f"http://{addr.baseURL}/media/{obj.img}"]

    def get_text_par(self, obj):
        return obj.text.splitlines()

    def get_aid(self, obj):
        return obj.id


class PictureSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            'pictureurl',
        )

    def get_pictureurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.img}"
