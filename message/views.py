from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from pkg.auth import require_login
from .models import Message
from .serializers import MessageTitleSerializer, MessageContextSerializer

import pprint


class MessageTitleView(APIView):
    def get(self, request):
        category = request.data.get('category') or request.GET.get('category') or 0
        if int(category) == 0:
            return Response(MessageTitleSerializer(Message.objects.all().order_by('-create_time'), many=True).data)
        return Response(
            MessageTitleSerializer(Message.objects.filter(category=category).order_by('-create_time'), many=True).data)

    @require_login
    def post(self, request):
        title = request.data.get('title')
        text = request.data.get('text')
        category = request.data.get('category')
        create_time = request.data.get('create_time') or timezone.now()
        if not title:
            return Response({"detail": "请输入文章标题"}, status=status.HTTP_400_BAD_REQUEST)
        if not text:
            return Response({"detail": "请输入文章内容"}, status=status.HTTP_400_BAD_REQUEST)
        if not category:
            return Response({"detail": "未指定所属板块"}, status=status.HTTP_400_BAD_REQUEST)
        Message.objects.create(title=title, text=text, create_time=create_time, category=category)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class MessageContextView(APIView):
    def get(self, request):
        aid = request.data.get('aid') or request.GET.get('aid')
        if not aid:
            return Response({"detail": "未指定文章编号"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MessageContextSerializer(Message.objects.filter(id=aid), many=True).data)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        aid = request.data.get('aid')
        if not aid:
            return Response({"detail": "未指定文章编号"}, status=status.HTTP_400_BAD_REQUEST)
        Message.objects.filter(id=aid).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
