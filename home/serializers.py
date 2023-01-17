from rest_framework import serializers

from .models import Home

from config import addr


class HomeSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()
    pid = serializers.SerializerMethodField()

    class Meta:
        model = Home
        fields = (
            'pictureurl', 'pid'
        )

    def get_pictureurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.img}"

    def get_pid(self, obj):
        return obj.id
