from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pkg.check_file import check_file_suffix
from .models import Home
from .serializers import HomeSerializer

from pkg.auth import require_login


class PictureView(APIView):

    def get(self, request):
        return Response(HomeSerializer(Home.objects.all(), many=True).data)

    @require_login
    def post(self, request):
        img = request.FILES.get('img') or request.FILES.get('file')
        if not img:
            return Response({"detail": "请选择要上传的文件"}, status=status.HTTP_400_BAD_REQUEST)
        if not check_file_suffix(img, ["jpg", "jpeg", "png"]):
            return Response({"detail": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        Home.objects.create(img=img)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Home.objects.get(id=pid).delete()
        except Exception as e:
            return Response({"detail": "数据不存在", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
