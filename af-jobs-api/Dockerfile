FROM python:3.9-slim-buster
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

ENV LOG_LEVEL info


RUN apt-get update

COPY . /app/
ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app/

RUN pip3 install  -r requirements.txt