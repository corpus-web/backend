from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from pkg.auth import require_login
from pkg.check_file import check_file_suffix
from .models import Meeting
from .serializers import MeetingTitleSerializer, MeetingContentSerializer, PictureSerializer


class ListView(APIView):
    def get(self, request):
        current_page = request.data.get('current_page') or request.GET.get('current_page') or 1
        max_num = request.data.get('max_num') or request.GET.get('max_num') or 1e6
        if int(current_page) <= 0:
            return Response({"detail": "页码不合法"}, status=status.HTTP_400_BAD_REQUEST)
        if int(max_num) <= 0:
            return Response({"detail": "每页显示条目数不合法"}, status=status.HTTP_400_BAD_REQUEST)
        total = Meeting.objects.count()
        return Response({"total": total, "data": MeetingTitleSerializer(
            Meeting.objects.all().order_by('-create_time')[
            (int(current_page) - 1) * int(max_num):int(current_page) * int(max_num)],
            many=True).data}, status=status.HTTP_200_OK)

    @require_login
    def post(self, request):
        title = request.data.get('title')
        img = request.FILES.get('img') or request.FILES.get('file')
        abstract = request.data.get('abstract')
        text = request.data.get('text')
        create_time = request.data.get('create_time') or timezone.now()
        if not title or not img or not abstract or not text:
            return Response({"detail": "请完整填写信息"}, status=status.HTTP_400_BAD_REQUEST)
        if not check_file_suffix(img, ["jpg", "jpeg", "png"]):
            return Response({"detail": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        Meeting.objects.create(title=title, img=img,
                               abstract=abstract, text=text, create_time=create_time)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class ContentView(APIView):
    def get(self, request):
        aid = request.data.get('aid') or request.GET.get('aid')
        if not aid:
            return Response({"detail": "未获取查询条件"}, status=status.HTTP_400_BAD_REQUEST)
        if not Meeting.objects.filter(id=aid):
            return Response({"detail": "未查询到数据"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MeetingContentSerializer(Meeting.objects.filter(id=aid), many=True).data)


class PictureView(APIView):
    def get(self, request):
        return Response(PictureSerializer(Meeting.objects.all(), many=True).data)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        aid = request.data.get('aid')
        if not aid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Meeting.objects.get(id=aid).delete()
        except Exception as e:
            return Response({"detail": "数据不存在", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
