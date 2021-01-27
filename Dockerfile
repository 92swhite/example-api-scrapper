FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install libpq-dev -y &&\
    apt-get install python-dev -y &&\
    apt-get install gcc -y &&\
    apt-get install curl -y &&\
    mkdir /code &&\
    mkdir /code/scraper &&\
    mkdir /code/kafka

COPY requirements.txt /code

RUN pip3 install -r /code/requirements.txt && \
    rm -r /root/.cache

COPY /example-api-scrapper/. /code/scraper/

COPY /kafka/. /code/kafka/

WORKDIR /code/scraper

ENTRYPOINT ["python", "main.py"]