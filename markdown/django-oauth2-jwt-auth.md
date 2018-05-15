title: Django OAuth2 和 JWT 案例
date: 2017-08-08 20:34:21
---

在重写 Ansible 监控平台时， 需要前后端分离， 并且需要使用公司的账户系统。 而前后端认证我一直采取的 JWT 认证规范，具体为什么这么选择， 这里不多讲。而符合`DRF` 的JWT 框架， 默认使用的是 Django 自带的账户系统做的。 所以再 OAuth2 和 JWT 结合需要做点工作。

**OAuth2认证方法**

> 此步骤主要包含， 从资源服务器交换 Token， 然后根据 token 获取当前用户的 profile 信息， 一般为 email 和 avatar 信息. 然后创建 Django 自带的 User。 也可以通过函数实现。

```python
# -*- coding: utf-8 -*-

"""
web.auth
~~~~~~~~

Cable 认证组件

这里只接受 code， 通过 code 及相对应的密钥换取 Token 后

获取用户信息， 并根据数据库是否有此用户。

如果没有此用户则创建， 并设置未激活状态

如果有此用户， 并且处于未激活状态， 则提示用户找管理员激活

如果已经激活， 返回登录此用户并返回 jwt.
"""

import requests
from web.models import Profile
from web.models import User
from rest_framework.exceptions import APIException


class TeambitionAuthenticationFailed(APIException):
    status_code = 401
    default_code = 'Unauthorized'


class CableOAuth2(object):

    access_token_url = "https://account.teambition.com/oauth2/access_token"
    user_profile_url = "https://api.teambition.com/api/users/me"

    def __init__(self, CK, SK):
        self.CK = CK
        self.SK = SK

    def get_profile(self, email=""):
        profile = Profile.objects.filter(user__email=email).first()

        return profile

    def get_user(self, email=""):
        user = User.objects.filter(email=email).first()

        return user

    def is_actived(self, user):
        return user.is_active

    def get_access_token(self, code):
        payload = {
            'client_id': self.CK,
            'client_secret': self.SK,
            'code': code,
            'grant_type': 'Bearer'
        }

        resp = self.request(
            "POST",
            self.access_token_url,
            data=payload
        )

        data = resp.json()
        return data.get('access_token', None)

    def get_me(self, access_token):
        """
        获取用户信息
        """
        resp = self.request(
            "GET",
            self.user_profile_url + '?access_token=' + access_token
        )

        return resp.json()

    def request(self, method, url, **kwargs):
        resp = requests.request(method, url, **kwargs)

        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            m = resp.json()

            detail = "%s %s" % (url, str(e))
            if 'message' in m and 'name' in m:
                detail = "%s %s" % (m["name"], m["message"])

            raise TeambitionAuthenticationFailed(detail)
        return resp

    def authentication(self, code):
        access_token = self.get_access_token(code)

        # 如果没有获取到 access token 那么后面就不继续了
        # 直接报错给客户端
        if not access_token:
            detail = "Get access token failure"
            raise TeambitionAuthenticationFailed(detail)

        me = self.get_me(access_token)

        # 这里做下安全保护， 如果非 teambition 域名的用户
        # 直接返回， 并给出非法警告.
        if not me["email"].endswith('teambition.com'):
            detail = "非法操作, 您不是 teambtion 员工，请立即停止此行为!!"
            raise TeambitionAuthenticationFailed(detail)

        user = self.get_user(me["email"])
        profile = self.get_profile(me["email"])

        if not user:
            user = User(
                username=me["email"].split("@")[0],
                email=me["email"],
                is_active=False
            )

            user.save()

        profile_data = {
            "avatar": me["avatarUrl"]
        }

        Profile.objects.update_or_create(user=user, defaults=profile_data)

        return user
```

**JWT APIView***

引入的包

```python
from django.utils.translation import ugettext as _
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.serializers import Serializer
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.serializers import jwt_get_username_from_payload
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.views import jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from web.auth import CableOAuth2
```

> 由于 OAuth2 返回时仅返回 code， 所以需要在`JWTSerializer`中获取此 code 并通过上面方法认证.

```python
class TeambitionJWTSerializer(Serializer):

    def validate(self, attrs):
        code = self.initial_data.get("code", None)

        oa = CableOAuth2(CK=settings.OAUTH_CLIENT_KEY, SK=settings.OAUTH_SECRET_KEY)

        user = oa.authentication(code)

        if user:
            if not user.is_active:
                msg = _('User account is not actived or disabled.')
                raise serializers.ValidationError(msg)

            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)
```

> 默认的 JWT APIView 方法是 POST， OAuth2 Callback URL 是 GET 方式， 所以需要自定义个`JWTView`， 目的是通过回调ˇ GET 的方式获得 Code.

```python
class TeambitionJWTAPIView(JSONWebTokenAPIView):

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**绑定到 Serializer**

```
class TeambitionObtainJSONWebToken(TeambitionJWTAPIView):
    serializer_class = TeambitionJWTSerializer


teambition_obtain_jwt_token = TeambitionObtainJSONWebToken.as_view()
```

**替换默认的签发路径**

> 并把资源服务的应用程序回掉地址改为`http://<host:port>/jwt/teambition/obtain`

```python
from django.conf.urls import url, include
from web.auth.jwt import teambition_obtain_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


urlpatterns = [
    # oauth2 
    url(r'^jwt/teambition/obtain', teambition_obtain_jwt_token),

    # username & password auth
    # url(r'^jwt/obtain', obtain_jwt_token),
    url(r'^jwt/refresh', refresh_jwt_token),
    url(r'^jwt/verify', verify_jwt_token),
]
```
