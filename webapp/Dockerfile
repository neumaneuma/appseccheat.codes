FROM python:latest

WORKDIR /app

EXPOSE 5000 8000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
