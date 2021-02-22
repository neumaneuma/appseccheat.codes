from sqlite3.dbapi2 import Error
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
    my_database = db.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = my_database.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'").fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)

@app.route("/patches/login", methods=["POST"])
def loginSecureLogin():
    my_database = db.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = my_database.execute("SELECT id FROM user WHERE username = :username AND password = :password", {"username" :username, "password" :password}).fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)

@app.route("/vulnerabilities/register", methods=["POST"])
def register():
    my_database = db.get_db()
    username = request.form["username"]
    password = request.form["password"]
    try:
        my_database.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    except Error as e:
        # to do need to decide how to handle errors
        return (repr(e), 400)
    return ("Success (1/2)", 200)

