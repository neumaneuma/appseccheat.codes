from flask import Flask
from flask import request
import os
from . import db
# from .sqli1 import login
# from vulnerabilities.sqli1 import sqli1

app = Flask(__name__)
# app.register_blueprint(sqli1.bp)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/vulnerabilities/login", methods=["POST"])
def login():
    return request.form['username']
