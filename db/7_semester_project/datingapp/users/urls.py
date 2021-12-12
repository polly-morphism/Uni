from django.urls import path, include
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from . import views

urlpatterns = [
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", views.login_view, name="login"),
    path("refresh/", views.refresh_token_view, name="refresh_token"),
    path("is_auth/", views.IsAccessToken, name="isAuth"),
    # path("get_icons/", views.GetIcons.as_view()),
    path("logout/", views.LogoutView),
    path(
        "update_profile/", views.UpdateProfileView.as_view(), name="auth_update_profile"
    ),
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path("change_photo/", views.ChangeUserPhoto.as_view()),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
