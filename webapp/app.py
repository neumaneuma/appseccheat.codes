from flask import Flask
from flask import request
# from .sqli1 import login
# from vulnerabilities.sqli1 import sqli1

app = Flask(__name__)
# app.register_blueprint(sqli1.bp)

@app.route("/")
def index():
    return app.send_static_file("index.html")
# /login
@app.route("/vulnerabilities/login", methods=["POST"])
def login():
    return request.form['username']