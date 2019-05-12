# Image de base
FROM alpine:latest

# Installation de curl avec apt-get

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*


# Changement du repertoire courant
WORKDIR /app

ONBUILD COPY . /app
ONBUILD RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt


# On expose le port 3000
EXPOSE 4000

CMD ["/env/bin/python", "__init__.py"]
