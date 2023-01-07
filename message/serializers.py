from rest_framework import serializers

from .models import Message


class MessageTitleSerializer(serializers.ModelSerializer):
    aid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Message
        fields = (
            'aid', 'title', 'create_time', 'category'
        )

    def get_aid(self, obj):
        return obj.id


class MessageContextSerializer(serializers.ModelSerializer):
    aid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")
    text_par = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'aid', 'title', 'create_time', 'text_par'
        )

    def get_aid(self, obj):
        return obj.id

    def get_text_par(self, obj):
        return obj.text.splitlines()
