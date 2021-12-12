from django.urls import path, include
from . import views

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registartion"),
    # path("login/", views.login_view, name="login"),
    # path("logout/", views.LogoutView),
    # path(
    #     "update_profile/", views.UpdateProfileView.as_view(), name="auth_update_profile"
    # ),
]
