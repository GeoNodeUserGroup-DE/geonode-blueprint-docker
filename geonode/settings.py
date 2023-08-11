#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#

# Load default settings
from geonode.settings import *


#DEBUG = "False"


# Upload Settings
DEFAULT_MAX_UPLOAD_SIZE = "1073741824"  # 1GB
DEFAULT_MAX_PARALLEL_UPLOADS_PER_USER = 5


# Adminstrator Settings
ADMIN_EMAIL = "admin@localhost"
ADMIN_PASSWORD = "admin"
ADMIN_USERNAME = "admin"


# Account Registration Settings
ACCOUNT_OPEN_SIGNUP = "False"
ACCOUNT_APPROVAL_REQUIRED = "False"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = "False"
ACCOUNT_EMAIL_REQUIRED = "True"
ACCOUNT_EMAIL_VERIFICATION = "none"


# E-Mail Settings
EMAIL_ENABLE = "True"
EMAIL_HOST = "localhost"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = "25"
EMAIL_USE_SSL = "False"
EMAIL_USE_TLS = "False"
DEFAULT_FROM_EMAIL = "GeoNode <no-reply@geonode.org>"
