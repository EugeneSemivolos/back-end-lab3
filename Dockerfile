FROM python:3.10.11-slim-bullseye

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /src

WORKDIR /src

ENV FLASK_APP=src/__init__


CMD flask run -h 0.0.0.0 -p $PORT