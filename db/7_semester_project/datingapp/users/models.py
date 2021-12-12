from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
import os


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    email_plaintext_message = "{}?token={}".format(
        os.environ.get("SERVER_URL"), reset_password_token.key
    )

    send_mail(
        # title:
        "Password Reset for {title}".format(title="dashboard"),
        # message:
        email_plaintext_message,
        # from:
        os.environ.get("from_email"),
        # to:
        [reset_password_token.user.email],
    )


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=2000, blank=True)

    def user_id(self):
        return self.id.__str__()

    def delete(self, *args, **kwargs):
        self.photo.delete(save=False)
        super(User, self).delete(*args, **kwargs)


class BlackenTokens(models.Model):
    token = models.CharField(max_length=512)


class MediaFiles(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=512)
    image = models.FileField()
