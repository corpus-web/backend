from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from pkg.auth import require_login
from pkg.check_file import check_file_suffix
from .models import Prize
from .serializers import MultiSerializer
from .utils import order


class PrizeView(APIView):
    def get(self, request):
        return Response(order.process(MultiSerializer(Prize.objects.all().order_by('-prize_time'), many=True).data))

    @require_login
    def post(self, request):
        prize_time = request.data.get('prize_time') or timezone.now()
        img = request.FILES.get('img') or request.FILES.get('file')
        text = request.data.get('text')
        if not img:
            return Response({"detail": "请选择要上传的图片"}, status=status.HTTP_400_BAD_REQUEST)
        if not check_file_suffix(img, ["jpg", "jpeg", "png"]):
            return Response({"detail": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        if not text:
            return Response({"detail": "请输入该证书的详细描述"}, status=status.HTTP_400_BAD_REQUEST)
        Prize.objects.create(prize_time=prize_time, img=img, text=text)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Prize.objects.get(id=pid).delete()
        except Exception as e:
            return Response({"detail": "数据不存在", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class PrizeViews(APIView):
    def get(self, request):
        return Response(MultiSerializer(Prize.objects.all().order_by('-prize_time'), many=True).data)
