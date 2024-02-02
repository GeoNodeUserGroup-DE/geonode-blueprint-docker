#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#


#DEBUG = "False"


# sets defaults settings and from .env
from geonode.settings import *
from geonode.settings import TEMPLATES, INSTALLED_APPS


SITENAME = os.getenv("SITENAME", "geonode")
X_FRAME_OPTIONS = "SAMEORIGIN"
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
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d "
            "%(thread)d %(message)s"
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
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
            "level": "DEBUG",
        },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "geonode_logstash.logstash": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}


INSTALLED_APPS += (
    "externalapplications",
    "customizations",
)
