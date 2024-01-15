FROM python:3.8-slim-buster

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN MKDIR /registration
COPY . /registration
WORKDIR /registration
COPY . .

CMD gunicorn --bind 0.0.0.0:8103 wsgi:app