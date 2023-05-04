from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pkg.auth import require_login
from pkg.check_file import check_file_suffix
from .utils import dbSearch
from .models import Picture, Category, File
from .serializers import PictureSerializer, FileSerializer, CategorySerializer
import chardet


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


class FormatView(APIView):
    def get(self, request):
        word_or_regex = request.GET.get('word_or_regex')
        limit_case = request.GET.get('limit_case') or 0
        category = request.GET.get('category') or 0
        query_method = request.GET.get('query_method') or 0
        if not word_or_regex:
            return Response({"detail": "请输入有效的信息"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            dbSearch.get_frequency_list(
                word_or_regex=word_or_regex,
                limit_case=limit_case,
                category=category,
                query_method=query_method
            ),
            status=status.HTTP_200_OK
        )


class CategoryView(APIView):
    def get(self, request):
        ret_list = CategorySerializer(Category.objects.all(), many=True).data
        # normal_list = [{
        #     "cid": 0,
        #     "name": "全部",
        #     "name_en": "ALL"
        # }]
        # ret_list_1 = normal_list + ret_list
        return Response({"a": ret_list}, status=status.HTTP_200_OK)

    def post(self, request):
        category_cn = request.data.get('name')
        category_en = request.data.get('name_en')
        if not category_en or not category_cn:
            return Response({"detail": "类别名称填写不完整"}, status=status.HTTP_400_BAD_REQUEST)
        if Category.objects.filter(Q(name=category_cn) | Q(name_en=category_en)).count():
            return Response({"detail": "该类别已存在"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Category.objects.create(name=category_cn, name_en=category_en)
        except Exception as e:
            return Response({"detail": "类别创建失败", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_201_CREATED)


class FileView(APIView):
    def get(self, request):
        category = request.GET.get('category') or 0
        page = request.GET.get('page') or 1
        per_page = request.GET.get('per_page') or 50
        page_start = (int(page) - 1) * int(per_page)
        page_end = int(page) * int(per_page)
        try:
            if int(category) == 0:
                query_set = File.objects.all()
                total = query_set.count()
                return Response(
                    {
                        "total": total,
                        "data": FileSerializer(query_set[page_start:page_end], many=True).data
                    }, status=status.HTTP_200_OK
                )
            else:
                query_set = File.objects.filter(category_id=category)
                total = query_set.count()
                return Response(
                    {
                        "total": total,
                        "data": FileSerializer(query_set[page_start:page_end], many=True).data
                    }, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response({"detail": "未选择分类", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FileViews(APIView):
    def get(self, request):
        word_or_regex = request.GET.get('word_or_regex')
        limit_case = request.GET.get('limit_case') or 0
        category = request.GET.get('category') or 0
        page = request.GET.get('page') or 1
        per_page = request.GET.get('per_page') or 10
        window_size = request.GET.get('window_size') or 50
        query_method = request.GET.get('query_method') or 0
        if word_or_regex:
            res_list = dbSearch.get_essay_list_by_word(
                word=word_or_regex,
                limit_case=limit_case,
                category=category,
                page=page,
                per_page=per_page,
                window_size=window_size,
                query_method=query_method
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
        try:
            encoding = chardet.detect(text)['encoding'] or 'utf-8'
            text_decode = text.decode(encoding, errors='ignore')
            # text_encode = text_decode.encode('utf-8')
            text_format = str(text_decode).replace("\r", " ").replace("\n", " ")
        except Exception as e:
            return Response({"detail": "文件解析失败", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        category_id = request.data.get('category') or 1
        _category = Category.objects.get(id=category_id)
        sub_name = request.data.get('sub_name')
        try:
            File.objects.create(
                name=name,
                sub_name=sub_name,
                category=_category,
                text=text_format
            )
        except Exception:
            return Response({"detail": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_201_CREATED)


class DeleteView(APIView):
    @require_login
    def post(self, request, nid):
        if nid == 1:
            fid = request.data.get('fid')

            if not fid:
                return Response({"detail": "未获取到文章编号"}, status=status.HTTP_400_BAD_REQUEST)
            file = File.objects.filter(id=fid)
            if not file.count():
                return Response({"detail": "文章不存在"}, status=status.HTTP_400_BAD_REQUEST)
            file.delete()
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        elif nid == 2:
            cid = request.data.get('cid')
            if not cid:
                return Response({"detail": "未获取类别编号"}, status=status.HTTP_400_BAD_REQUEST)
            if not Category.objects.filter(id=cid).count():
                return Response({"detail": "该类别不存在"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                Category.objects.filter(id=cid).delete()
            except Exception as e:
                return Response({"detail": "该类别下有未删除的文章", "error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        elif nid == 3:
            pid = request.data.get('pid')
            if not pid:
                return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                Picture.objects.get(id=pid).delete()
            except Exception as e:
                return Response({"detail": "数据不存在", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "无效的操作"}, status=status.HTTP_404_NOT_FOUND)
