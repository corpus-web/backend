from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pkg.auth import require_login
from pkg.check_file import check_file_suffix
from .utils import dbSearch
from .models import Picture, Category, File
from .serializers import PictureSerializer, FileSerializer


class TestView(APIView):
    def get(self, request):
        return Response({"detail": "ok"})


class PictureView(APIView):
    def get(self, request):
        return Response(PictureSerializer(Picture.objects.all(), many=True).data)

    @require_login
    def post(self, request):
        img = request.FILES.get('img') or request.FILES.get('file')
        if not img:
            return Response({"detail": "请选择要上传的文件"}, status=status.HTTP_400_BAD_REQUEST)
        if not check_file_suffix(img, ["jpg", "jpeg", "png"]):
            return Response({"detail": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        Picture.objects.create(img=img)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
    def delete(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        Picture.objects.filter(id=pid).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class FormatView(APIView):
    def get(self, request):
        word_or_regex = request.GET.get('word_or_regex')
        limit_case = request.GET.get('limit_case') or 0
        category = request.GET.get('category') or 0
        query_method = request.GET.get('query_method') or 0
        return Response(
            dbSearch.get_frequency_list(
                word_or_regex=word_or_regex,
                limit_case=limit_case,
                category=category,
                query_method=query_method
            ),
            status=status.HTTP_200_OK
        )


class FileView(APIView):
    def get(self, request):
        category = request.GET.get('category') or 0
        page = request.GET.get('page') or 1
        per_page = request.GET.get('per_page') or 50
        page_start = (int(page) - 1) * int(per_page)
        page_end = int(page) * int(per_page)
        if int(category) == 0:
            query_set = File.objects.all()
            total = query_set.count()
            return Response(
                {
                    "total": total,
                    "data": FileSerializer(query_set[page_start:page_end], many=True).data
                }, status=status.HTTP_200_OK
            )
        elif int(category) == 1:
            query_set = File.objects.filter(category_id=1)
            total = query_set.count()
            return Response(
                {
                    "total": total,
                    "data": FileSerializer(query_set[page_start:page_end], many=True).data
                }, status=status.HTTP_200_OK
            )
        elif int(category) == 2:
            query_set = File.objects.filter(category_id=2)
            total = query_set.count()
            return Response(
                {
                    "total": total,
                    "data": FileSerializer(query_set[page_start:page_end], many=True).data
                }, status=status.HTTP_200_OK
            )
        return Response({"detail": "未选择分类"}, status=status.HTTP_400_BAD_REQUEST)


class FileViews(APIView):
    def get(self, request):
        word_or_regex = request.GET.get('word_or_regex')
        limit_case = request.GET.get('limit_case') or 0
        random_case = request.GET.get('random_case') or 0
        category = request.GET.get('category') or 0
        page = request.GET.get('page') or 1
        per_page = request.GET.get('per_page') or 10
        window_size = request.GET.get('window_size') or 50
        if word_or_regex:
            res_list = dbSearch.get_essay_list_by_word(
                word=word_or_regex,
                limit_case=limit_case,
                random_case=random_case,
                category=category,
                page=page,
                per_page=per_page,
                window_size=window_size
            )
            return Response(res_list, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "未输入要查询的单词"}, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request):
        file = request.FILES.get('file')
        if not check_file_suffix(file, ["txt"]):
            return Response({"detail": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        name = file.name
        text = file.read()
        category_id = request.data.get('category') or 1
        _category = Category.objects.get(id=category_id)
        sub_name = request.data.get('sub_name')
        try:
            File.objects.create(
                name=name,
                sub_name=sub_name,
                category=_category,
                text=text
            )
        except Exception:
            return Response({"detail": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_201_CREATED)

    @require_login
    def delete(self, request):
        fid = request.data.get('fid')
        if not fid:
            return Response({"detail": "未获取到文章编号"}, status=status.HTTP_400_BAD_REQUEST)
        file = File.objects.filter(id=fid)
        if not file.count():
            return Response({"detail": "文章不存在"}, status=status.HTTP_400_BAD_REQUEST)
        file.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
