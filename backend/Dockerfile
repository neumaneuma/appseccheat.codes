FROM python:3.12

WORKDIR /app

EXPOSE 12300 8000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
