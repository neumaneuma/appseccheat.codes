FROM python:3.13.0

WORKDIR /app

EXPOSE 12301

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
