FROM python:3.9.2

WORKDIR /app

EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# need to figure out how to handle development and production without maintaining 2 different docker files
ENV FLASK_ENV="development"
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
