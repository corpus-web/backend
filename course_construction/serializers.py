from rest_framework import serializers

from .models import Course

from config import addr


class CourseSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField()
    pid = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'pid', 'pictureurl'
        )

    def get_pictureurl(self, obj):
        return f"http://{addr.baseURL}/media/{obj.img}"

    def get_pid(self, obj):
        return obj.id
