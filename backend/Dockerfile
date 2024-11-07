FROM python:3.13.0

WORKDIR /backend

EXPOSE 12300

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
