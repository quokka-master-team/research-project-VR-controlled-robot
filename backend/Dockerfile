FROM python:3.11-alpine

WORKDIR /home/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements /tmp/requirements

RUN apk --update add  \
    bash  \
    gcc  \
    libc-dev  \
    libffi-dev  \
    postgresql-client

RUN set -ex \
    && wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh" -O /usr/bin/wait-for-it \
    && chmod +x /usr/bin/wait-for-it

RUN pip install -r /tmp/requirements/base.txt
RUN pip install -r /tmp/requirements/lint.txt
