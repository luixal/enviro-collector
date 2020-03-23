FROM python:3.8.2-slim-buster

LABEL maintainer="Luis Alberto Pérez García <luixal@gmail.com>" \
      version="0.1.1" \
      description="Reads and sends info from an Enviro sensor on a RaspberryPi to an HTTP backend" \
      repo="https://github.com/luixal/enviro-collector"

COPY ./src/* /app/
WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  python-numpy \
  python-smbus \
  python-pil \
  python-setuptools \
  libportaudio2 \
  libffi-dev

RUN pip3 install enviroplus requests smbus smbus2 sounddevice numpy

CMD python /app/enviro_collector.py
