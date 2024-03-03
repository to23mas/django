FROM python:3.11.4-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
