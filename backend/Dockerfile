FROM python:3.11-slim-bookworm

WORKDIR /home/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements /tmp/requirements

RUN apt-get update && apt-get upgrade
RUN apt-get install -y bash  \
    wget \
    gcc  \
    libc-dev  \
    libffi-dev  \
    postgresql-client \
    ffmpeg

RUN set -ex \
    && wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh" -O /usr/bin/wait-for-it \
    && chmod +x /usr/bin/wait-for-it

RUN pip install -r /tmp/requirements/base.txt
RUN pip install -r /tmp/requirements/lint.txt
