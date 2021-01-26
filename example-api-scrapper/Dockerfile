FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code/
WORKDIR /code
COPY . /code/

RUN apt-get update &&\
    apt-get install libpq-dev -y &&\
    apt-get install python-dev -y &&\
    apt-get install gcc -y &&\
    apt-get install curl -y &&\
    pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]