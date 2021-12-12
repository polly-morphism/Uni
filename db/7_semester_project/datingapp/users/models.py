from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=2000, blank=True)

    def user_id(self):
        return self.id.__str__()

    def delete(self, *args, **kwargs):
        self.photo.delete(save=False)
        super(User, self).delete(*args, **kwargs)
