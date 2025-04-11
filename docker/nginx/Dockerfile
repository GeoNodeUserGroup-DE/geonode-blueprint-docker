ARG BASE_IMAGE_VERSION
FROM geonode/nginx:${BASE_IMAGE_VERSION}
ARG CERT_PATH_CHAIN=./cert.pem
ARG CERT_PATH_KEY=./key.pem

ENV STATIC_ROOT=/mnt/volumes/statics/static/
ENV MEDIA_ROOT=/mnt/volumes/statics/uploaded/

# use $http_host variable instead of $host which does not transport the port
COPY ./geonode.conf.envsubst /etc/nginx/sites-enabled/geonode.conf.envsubst
# overwrite nginx conf for hardening
COPY ./nginx.https.available.conf.envsubst /etc/nginx/nginx.https.available.conf.envsubst
