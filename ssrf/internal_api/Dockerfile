FROM python:3.9.7

WORKDIR /app

EXPOSE 8484

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
