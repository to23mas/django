FROM python:3.11.4-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install cron and other dependencies
# The rm -rf command removes apt cache to reduce image size - best practice for Docker images
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt
COPY .env /etc/environment

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create log file and set permissions
RUN touch /var/log/cron.log && chmod 0644 /var/log/cron.log
