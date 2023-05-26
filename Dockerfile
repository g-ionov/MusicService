FROM python:3.10-alpine3.17
ENV PYTHONUNBUFFERED 1

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000

RUN adduser --disabled-password service-user
USER service-user