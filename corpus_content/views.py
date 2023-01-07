import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from corpus_web.settings import BASE_DIR
from pkg.auth import require_login
from .utils import simpleSearch
from .models import ArticlePost, Picture
from .serializers import ArticlePostSerializer, PictureSerializer


class TestView(APIView):
    def get(self, request):
        return Response({"detail": "ok"})


class FileView(APIView):
    def get(self, request):
        return Response(ArticlePostSerializer(ArticlePost.objects.all(), many=True).data)

    @require_login
    def post(self, request):
        title = request.data.get('title') or 'normal'
        author = request.data.get('author') or 'normal'
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "请上传文件"}, status=status.HTTP_400_BAD_REQUEST)
        elif '.txt' not in file._get_name():
            return Response({"detail": "不支持的文件类型"}, status=status.HTTP_400_BAD_REQUEST)
        ArticlePost.objects.create(title=title, author=author, file=file)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
    def delete(self, request):
        article_id = request.data.get('fid')
        if not article_id:
            return Response({"detail": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
        if not ArticlePost.objects.filter(id=article_id):
            return Response({"detail": "未找到该文件"}, status=status.HTTP_400_BAD_REQUEST)
        file_path = "/media/" + str(ArticlePost.objects.get(id=article_id).file)
        os.remove(r"{}".format(str(BASE_DIR) + file_path))
        ArticlePost.objects.get(id=article_id).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class SearchView(APIView):
    def get(self, request):
        word = request.data.get('word') or request.GET.get('word')
        window_size = request.data.get('window_size') or request.GET.get('window_size') or 50
        current_page = request.data.get('current_page') or request.GET.get('current_page') or 1
        max_num = request.data.get('max_num') or request.GET.get('max_num') or 10
        category = request.data.get('category') or request.GET.get('category') or 0
        limitcase = request.data.get('limitcase') or request.GET.get('limitcase') or False
        randomcase = request.data.get('randomcase') or request.GET.get('randomcase') or False
        if not word:
            return Response({"detail": "请输入要查询的单词"}, status=status.HTTP_400_BAD_REQUEST)
        if int(window_size) <= len(word):
            return Response({"detail": "窗口大小设置不合法"}, status=status.HTTP_400_BAD_REQUEST)
        if int(current_page) <= 0:
            return Response({"detail": "页码不合法"}, status=status.HTTP_400_BAD_REQUEST)
        if int(max_num) <= 0:
            max_num = 1
        res_dict = simpleSearch.search(word, window_size, current_page, max_num, category, limitcase, randomcase)
        if not res_dict:
            return Response({"detail": "未查询到内容"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res_dict, status=status.HTTP_200_OK)


class SearchViews(APIView):

    def get(self, request):
        word = request.data.get('word') or request.GET.get('word')
        category = request.data.get('category') or request.GET.get('category') or 0
        limitcase = request.data.get('limitcase') or request.GET.get('limitcase') or False
        if not word:
            return Response({"detail": "请输入要查询的单词"}, status=status.HTTP_400_BAD_REQUEST)
        res_list, word_num = simpleSearch.search_new(word, category, limitcase)
        if not res_list:
            return Response({"detail": "未查询到内容"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(word_num, status=status.HTTP_200_OK)


class PictureView(APIView):
    def get(self, request):
        return Response(PictureSerializer(Picture.objects.all(), many=True).data)

    @require_login
    def post(self, request):
        img = request.FILES.get('img') or request.FILES.get('file')
        if not img:
            return Response({"detail": "请选择要上传的文件"}, status=status.HTTP_400_BAD_REQUEST)
        Picture.objects.create(img=img)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
    def delete(self, request):
        pid = request.data.get('pid')
        if not pid:
            return Response({"detail": "未指定要删除的数据"}, status=status.HTTP_400_BAD_REQUEST)
        Picture.objects.filter(id=pid).delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
