from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Home
from .serializers import HomeSerializer

from pkg.auth import require_login


class PictureView(APIView):

    def get(self, request):
        return Response(HomeSerializer(Home.objects.all(), many=True).data)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        Home.objects.filter(id=pid).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
