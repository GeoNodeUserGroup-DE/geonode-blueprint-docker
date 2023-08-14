#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#


#DEBUG = "False"

# sets defaults settings and from .env
from geonode.settings import *


# E-Mail Settings
EMAIL_ENABLE = "True"
EMAIL_HOST = "localhost"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = "25"
# either SSL ..
EMAIL_USE_SSL = "False"
# .. or TLS
EMAIL_USE_TLS = "False"
DEFAULT_FROM_EMAIL = "GeoNode <no-reply@geonode.org>"
