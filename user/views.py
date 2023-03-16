import base64
import io

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pkg import code, enctypt
from pkg.auth import require_login, gene_token, read_token
from .models import User
from .serializers import UserSerializer
import xml.etree.ElementTree as ET
from .utils.xml_process import element_to_dict


class LoginView(APIView):

    def get(self, request):
        img, code_str = code.gene_code()
        buffered = io.BytesIO()
        img.save(buffered, format='PNG')
        img_str = base64.b64encode(buffered.getvalue())
        md5_str = enctypt.md5(img_str, 1)
        code.cache_code(md5_str, code_str)
        return Response({"img": img_str}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        pwd = request.data.get('password')
        img_str = request.data.get('img')
        code_str = request.data.get('code')
        if not code_str or not img_str:
            return Response({"detail": "请输入验证码"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        md5_str = enctypt.md5(img_str, 2)
        res = bool(code.check_code(md5_str, str(code_str).upper()))
        if not res:
            return Response({"detail": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(username=username):
            return Response({"detail": "账号或密码错误"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        user = User.objects.get(username=username)
        if user.check_password(pwd):
            token = gene_token(user.username)
            return Response({"detail": "登录成功", "token": token})
        return Response({"detail": "账号或密码错误"}, status=status.HTTP_402_PAYMENT_REQUIRED)


class UserCreateView(APIView):
    @require_login
    def get(self, request):
        return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_200_OK)

    @require_login
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"detail": "请输入用户名和密码"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create_user(username=username, password=password)
        return Response({"detail": "success"}, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    @require_login
    def post(self, request):
        new_password = request.data.get('new_password')
        token = request.data.get("token") or request.META.get('HTTP_TOKEN')
        if not new_password:
            return Response({"detail": "请填写完整"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            username = read_token(token)
            if not username:
                return Response({"detail": "验证失败"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


class CasLoginView(APIView):
    def post(self, request):
        service = request.data.get('service')
        ticket = request.data.get('ticket')
        if not service or not ticket:
            return Response({"detail": "require 2 params"}, status=status.HTTP_400_BAD_REQUEST)
        cas_url = "https://cas.hrbeu.edu.cn/cas/serviceValidate"
        param_dict = {"service": service, "ticket": ticket}
        res = requests.get(url=cas_url, params=param_dict)
        # print(res.text)
        xml_str = str(res.text)
        xml_root = ET.fromstring(xml_str)
        xml_data = element_to_dict(xml_root)
        try:
            attr_dict = xml_data.get('{http://www.yale.edu/tp/cas}authenticationSuccess').get(
                '{http://www.yale.edu/tp/cas}attributes')
            user_name = attr_dict.get('{http://www.yale.edu/tp/cas}name')
            user_code = attr_dict.get('{http://www.yale.edu/tp/cas}username')
            data = {
                "user_name": user_name,
                "user_code": user_code,
            }
            return Response({"detail": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "验证失败", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
