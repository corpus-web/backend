from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pkg.auth import require_login
from .models import Course
from .serializers import CourseSerializer


class MainView(APIView):
    def get(self, request):
        return Response(CourseSerializer(Course.objects.all(), many=True).data)


class DeleteView(APIView):
    @require_login
    def post(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        Course.objects.filter(id=pid).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
