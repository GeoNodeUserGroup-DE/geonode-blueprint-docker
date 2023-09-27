ARG BASE_IMAGE_VERSION
FROM 52north/geonode-nginx:${BASE_IMAGE_VERSION}

COPY ./cert.pem /geonode-certificates/autoissued/fullchain.pem
COPY ./cert.pem /geonode-certificatess/autoissued/privkey.pem
