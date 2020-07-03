FROM python:3.7.8-alpine3.12 as base

RUN apk update && apk add --no-cache \
  gcc \
  musl-dev \
  libffi-dev \
  openssl-dev \
  zlib-dev \
  nodejs \
  jpeg-dev \
  libc-dev \
  libffi-dev \
  libpng-dev \
  libsass \
  nodejs-npm \
  postgresql-dev

ENV POETRY_VERSION=1.0.9

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/srv/

# Copy poetry.lock for caching
COPY poetry.lock pyproject.toml /usr/srv/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$WAGTAIL_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /usr/srv/

WORKDIR /usr/srv/app/

