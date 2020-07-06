FROM python:3.8.3-buster as base

RUN apt-get update && \
  apt-get install -y --no-install-recommends  \
  gcc \
  musl-dev \
  libffi-dev \
  libssl-dev \
  zlib1g-dev \
  nodejs \
  libjpeg-dev \
  linux-libc-dev \
  libpng-dev \
  libsass-dev \
  npm \
  postgresql-client

ENV POETRY_VERSION=1.0.9

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/srv/

# Copy poetry.lock for caching
COPY poetry.lock pyproject.toml /usr/srv/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$WAGTAIL_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /usr/srv/

WORKDIR /usr/srv/app/

