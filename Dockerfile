FROM python:3.12-slim-bullseye
WORKDIR /app

LABEL authors="Jephte_Dunia"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT [ "gunicorn", "eventplan_core.wsgi" ]

