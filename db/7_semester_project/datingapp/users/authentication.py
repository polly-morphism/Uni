import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    """
    custom authentication class for DRF and JWT
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    PUBLIC_URLS = [
        "/auth/password_reset/confirm/",
        "/auth/password_reset/",
        "/auth/password_reset/validate_token/",
    ]

    def authenticate(self, request):
        if request.path in self.PUBLIC_URLS:
            return (None, None)
        else:
            User = get_user_model()
            access_token = request.COOKIES.get("access")
            if not access_token:
                raise exceptions.AuthenticationFailed("No access token")
            try:

                payload = jwt.decode(
                    access_token, settings.SECRET_KEY, algorithms=["HS256"]
                )

            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed("access_token expired")
            except IndexError:
                raise exceptions.AuthenticationFailed("Token prefix missing")

            user = User.objects.filter(id=payload["user_id"]).first()
            if user is None:
                raise exceptions.AuthenticationFailed("User not found")

            if not user.is_active:
                raise exceptions.AuthenticationFailed("user is inactive")

            self.enforce_csrf(request)
            return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)
