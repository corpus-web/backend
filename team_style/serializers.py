from rest_framework import serializers

from .models import Prize

from config import addr


class MultiSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()
    prize_time = serializers.DateTimeField(format="%Y-%m-%d")
    pid = serializers.SerializerMethodField()

    class Meta:
        model = Prize
        fields = (
            'pid', 'pictureurl', 'prize_time', 'text',
        )

    def get_pictureurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.img}"

    def get_pid(self, obj):
        return obj.id
