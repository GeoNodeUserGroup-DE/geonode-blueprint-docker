ARG BASE_IMAGE_VERSION
FROM geonode/geonode:${BASE_IMAGE_VERSION}

COPY ./requirements.txt /usr/src/more_requirements.txt
RUN yes w | pip install --src /usr/src -r /usr/src/more_requirements.txt

#RUN rm .env*
