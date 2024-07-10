from .base import *  # noqa
from .base import INSTALLED_APPS, env  # noqa

DEBUG = True
INSTALLED_APPS = INSTALLED_APPS + []

ALLOWED_HOSTS = ["*"]

GEMINI_SYSTEM_INSTRUCTION = """
You are a model trained for auto replies to comments on posts.
You have to briefly answer to user's comments relatively to what they say and the content of the post itself.
"""
GEMINI_RPM = 15
GEMINI_TPM = 1_500

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

LOG_QUERIES = False

if LOG_QUERIES:
    LOGGING = {
        "version": 1,
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
                "handlers": ["console"],
            }
        },
    }
else:  # testing
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "formatters": {
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "loggers": {
            "": {  # This is the root logger
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }

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
