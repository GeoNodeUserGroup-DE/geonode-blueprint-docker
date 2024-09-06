#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#

import os
import ast
import sys


# sets defaults settings and from .env
from geonode.settings import *  # noqa
from geonode.settings import (  # noqa
    DEBUG,
    TEMPLATES,
    INSTALLED_APPS,
)

X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None if DEBUG else "same-origin"


# relax origins for geonode-mapstore-client development
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:8001",
    "http://localhost:8081"
] if DEBUG else ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]")) # noqa
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8001",
    "http://localhost:8081"
] if DEBUG else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))  # noqa


STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))


# Additional directories which hold static files
# - Give priority to local ones
TEMPLATES[0]["DIRS"].insert(0, "/usr/src/geonode/templates")
loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
TEMPLATES[0]["OPTIONS"]["loaders"] = loaders
TEMPLATES[0].pop("APP_DIRS", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},  # noqa
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geonode": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "owslib": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "pycsw": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geonode_logstash.logstash": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


INSTALLED_APPS += (
    "externalapplications",
    "customizations",
)
