FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

EXPOSE 8000
ENV LC_ALL=en_US.UTF8

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN mkdir -p /app/media
RUN mkdir -p /app/static
