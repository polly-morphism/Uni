import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import (
    UserSerializer,
    MediaSerializer,
    UpdateUserSerializer,
    ChangePasswordSerializer,
    ChangeUserAvatarSerializer,
)
from .utils import generate_access_token, generate_refresh_token
from rest_framework import generics
from .models import MediaFiles, BlackenTokens
from datetime import datetime, timedelta
from datingapp.utils import get_current_user


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
# @ensure_csrf_cookie
def login_view(request):
    """
    If ok returns dict with field status and user info
    """
    User = get_user_model()
    username = request.data.get("username")
    password = request.data.get("password")
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed("username and password required")

    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed("user not found")
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("wrong password")
    serialized_user = UserSerializer(user).data
    if serialized_user["is_active"]:
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        to_expires_date = datetime.now() + timedelta(days=5)
        to_expires_date = datetime.replace(to_expires_date, hour=0, minute=0, second=0)
        expires = datetime.strftime(to_expires_date, "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            expires=datetime.strftime(
                datetime.now() + timedelta(minutes=20), "%a, %d-%b-%Y %H:%M:%S GMT"
            ),
            samesite="Lax",
        )
        response.set_cookie(
            key="refreshtoken",
            value=refresh_token,
            httponly=True,
            expires=expires,
            samesite="Lax",
        )

        response.data = {
            "status": "ok",
            "user": serialized_user,
        }
    else:
        response.data = {
            "detail": "not active",
        }
    return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def refresh_token_view(request):
    """
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    """
    User = get_user_model()
    refresh_token = request.COOKIES.get("refreshtoken")
    if BlackenTokens.objects.filter(token=refresh_token):
        return Response("User is log out", status=status.HTTP_403_FORBIDDEN)

    response = Response()

    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            "Authentication credentials were not provided."
        )
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            "expired refresh token, please login again."
        )

    user = User.objects.filter(id=payload.get("user_id")).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found")

    if not user.is_active:
        raise exceptions.AuthenticationFailed("user is inactive")

    access_token = generate_access_token(user)
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        expires=datetime.strftime(
            datetime.now() + timedelta(minutes=20), "%a, %d-%b-%Y %H:%M:%S GMT"
        ),
    )
    serialized_user = UserSerializer(user).data

    response.data = {
        "status": "ok",
        "access_token": access_token,
        "user": serialized_user,
    }
    return response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def IsAccessToken(request):
    """
    This view is needed to check out access token
    """
    User = get_user_model()
    access_token = request.COOKIES.get("access")
    try:
        access_token = request.COOKIES.get("access")
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("access_token expired")
    except IndexError:
        raise exceptions.AuthenticationFailed("Token prefix missing")
    user = User.objects.filter(id=payload.get("user_id")).first()
    serialized_user = UserSerializer(user).data
    return Response(
        {
            "status": "ok",
            "user": serialized_user,
        }
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def LogoutView(request):
    refresh_token = request.COOKIES.get("refreshtoken")
    obj = BlackenTokens(token=refresh_token)
    obj.save()
    response = Response()
    response.delete_cookie("refreshtoken")
    return response


class GetIcons(generics.ListAPIView):
    queryset = MediaFiles.objects.all()
    serializer_class = MediaSerializer


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer

    def get_object(self):
        user = get_current_user(self.request)
        return user


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user = get_current_user(self.request)
        return user


class ChangeUserPhoto(generics.UpdateAPIView):

    serializer_class = ChangeUserAvatarSerializer

    def get_object(self):
        user = get_current_user(self.request)
        return user
