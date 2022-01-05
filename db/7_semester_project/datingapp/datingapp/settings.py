import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "b&e*xr@8z*oxpkn%8fsnx(**lk#xz+tz97q=5@gpy4n_8*r0w^"
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
#
# ALLOWED_HOSTS = []
SECRET_KEY = "b&e*xr@8z*oxpkn%8fsnx(**lk#xz+tz97q=5@gpy4n_8*r0w^"
DEBUG = 1
DJANGO_ALLOWED_HOSTS = "localhost 127.0.0.1 0.0.0.0 [::1]"


SQL_ENGINE = "django.db.backends.postgresql"
SQL_DATABASE = "db_project"
SQL_USER = "7semester"
SQL_PASSWORD = "db_project"
SQL_HOST = "db"
SQL_PORT = 5432
DATABASE = "postgres"

DJANGO_SU_NAME = "tAtiNgenScolEXcERito"
DJANGO_SU_EMAIL = "polina.verzun@innohubgroup.com"
DJANGO_SU_PASSWORD = "*kON1!YjTc!E42&7ZkRo"

# SECRET_KEY = SECRET_KEY

DEBUG = DEBUG

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS.split(" ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "datingprofile",
    "rest_framework",
    "django_rest_passwordreset",
    "corsheaders",
    "allauth",
    "rest_framework.authtoken",
    "users",
    "rest_auth",
    "drawio_django_model",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "datingapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "datingapp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": SQL_ENGINE,
        "NAME": SQL_DATABASE,
        "USER": SQL_USER,
        "PASSWORD": SQL_PASSWORD,
        "HOST": SQL_HOST,
        "PORT": SQL_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "http://app:8000",
    "http://app:3000",
    "http://localhost:5000",
    # "http://" + os.environ.get("SERVERIP") + ":5000",
    # "http://" + os.environ.get("SERVERIP") + ":3000",
    # "http://" + os.environ.get("SERVERIP") + ":8000",
)

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True


# AUTH SETTINGS FOR DRF

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
AUTH_USER_MODEL = "users.User"
REFRESH_TOKEN_SECRET = SECRET_KEY


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR + "/" + "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR + "/" + "mediafiles"

SITE_ID = 1
