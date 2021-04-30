FROM python:3.9.2

WORKDIR /app

EXPOSE 8181

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
