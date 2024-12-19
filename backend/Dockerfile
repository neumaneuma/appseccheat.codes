FROM --platform=$BUILDPLATFORM python:3.13.0-alpine

WORKDIR /backend

EXPOSE 12301

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
