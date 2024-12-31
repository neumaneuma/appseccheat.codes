FROM python:3.13.1-alpine

WORKDIR /internal_api

EXPOSE 12302

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
