from sqlite3.dbapi2 import Error
from flask import Flask
from flask import request
import os
from . import db as database
from webapp import sqli1

app = Flask(__name__)
app.register_blueprint(sqli1.vulnerability_bp)
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

database.init_app(app)


@app.route("/")
def index():
    return app.send_static_file("index.html")



@app.route("/patches/login", methods=["POST"])
def loginSecureLogin():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = db.execute("SELECT id FROM users WHERE username = :username AND password = :password", {"username" :username, "password" :password}).fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)


@app.route("/vulnerabilities/register", methods=["POST"])
def register():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
    except Error as e:
        # to do need to decide how to handle errors
        return (repr(e), 400)
    return ("Success (1/2)", 200)

@app.route("/vulnerabilities/change_password", methods=["POST"])
def change_password():
    db = database.get_db()
    original_username = "administrator"
    user_id = "2"
    old_password = request.form["old_password"]
    new_password = request.form["new_password1"]
    if new_password != request.form["new_password2"]:
        return ("Passwords do not match", 400)

    username = db.execute("SELECT username FROM users WHERE id = (?)", (user_id)).fetchone()[0]
    try:
        db.execute("UPDATE users SET password = :password1 WHERE username = '" + username + "' AND password = :password2", {"password1": new_password, "password2":old_password})
        db.commit()
    except Error as e:
        return (repr(e), 400)

    change_password_successful = db.execute("SELECT id FROM users WHERE username = :original_username AND password = :new_password", {"original_username" : original_username, "new_password" :new_password}).fetchone()

    return ("Success", 200) if change_password_successful else ("Failure", 400)
