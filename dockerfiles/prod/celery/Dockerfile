FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN mkdir "app"

WORKDIR app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./core .

EXPOSE 8000