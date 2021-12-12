from rest_framework import serializers
from .models import User, MediaFiles
from rest_framework.fields import UUIDField
from datingapp.utils import get_current_user
import django.contrib.auth.password_validation as validators
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "photo",
            "description",
        ]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFiles
        fields = ["name", "image"]


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user = get_current_user(self.context["request"])
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]

        instance.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = get_current_user(self.context["request"])
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


# I don't know  we need it, my test shows that with it we compress file from 1.7MB -> 15.1Kb, and without it also 1.7MB -> 15.2kB
def make_thumbnail(image):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    # im.convert("RGB")  # convert mode

    thumb_io = BytesIO()  # create a BytesIO object

    im.save(thumb_io, "JPEG", quality=90)  # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name)  # create a django friendly File object

    return thumbnail


class ChangeUserAvatarSerializer(serializers.ModelSerializer):
    photo = serializers.FileField()

    class Meta:
        model = User
        fields = ["photo"]

    def update(self, instance, validated_data):

        # image = make_thumbnail(validated_data["photo"])
        instance.photo.delete(save=False)
        photo_data = validated_data["photo"]
        instance.photo.save(f"{instance.username}_photo.jpg", photo_data, save=True)

        return instance
