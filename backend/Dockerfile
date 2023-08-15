FROM python:3.11.4-alpine

WORKDIR /home/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements /tmp/requirements

RUN apk --update add bash postgresql-client

RUN pip install -r /tmp/requirements/base.txt
RUN pip install -r /tmp/requirements/lint.txt
