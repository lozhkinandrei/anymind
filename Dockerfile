FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app
ENV PYTHONPATH=/app
