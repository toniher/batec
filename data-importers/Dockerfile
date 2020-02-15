FROM python:3.7.6-slim-buster
RUN apt-get update && apt-get -y upgrade

RUN mkdir -p /soft/app

COPY ./ /soft/app

WORKDIR /soft/app

RUN pip install -r requirements.txt

#VOLUME -> per a contrasenyes

