from .base import *  # noqa
from .base import INSTALLED_APPS, env

DEBUG = True
SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-4)*frn%aqqfc926x&g%s93_v^xx3btm7mcm1c&*pq3ilot-jbb")

INSTALLED_APPS = INSTALLED_APPS + []

ALLOWED_HOSTS = ["*"]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = {
    "SIGNING_KEY": SECRET_KEY,
}
