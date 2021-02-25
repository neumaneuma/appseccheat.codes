import uuid
from sqlite3.dbapi2 import Error
from flask import Blueprint, request, session
from .. import db as database
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli2", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli2"
)
username_to_exploit = "username_to_exploit_for_sqli2"
user_id_for_registered_account = "user_id_for_registered_account_for_sqli2"


@bp.route("/get_username", methods=["GET"])
def get_username_to_exploit():
    db = database.get_db()
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    username = username.replace("-", "")

    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    db.commit()

    session.pop(username_to_exploit, None)
    session[username_to_exploit] = username
    return username


@bp.route("/register", methods=["POST"])
def register():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        db.commit()
    except Error as e:
        return (repr(e), 400)

    user_id = db.execute(
        "SELECT id FROM users WHERE password = :password AND username = :username",
        {"password": password, "username": username},
    ).fetchone()

    session.pop(user_id_for_registered_account, None)
    session[user_id_for_registered_account] = str(user_id[0])
    return ("Success (1/2)", 200)


@bp.route("/change_password", methods=["POST"])
def change_password():
    db = database.get_db()
    if (
        username_to_exploit not in session
        or user_id_for_registered_account not in session
    ):
        return (
            "Session cookies are not found or have been modified. Either include them in the request or restart challenge.",
            400,
        )
    original_username = session[username_to_exploit]
    user_id = session[user_id_for_registered_account]
    old_password = request.form["old_password"]
    new_password = request.form["new_password1"]
    if new_password != request.form["new_password2"]:
        return ("Passwords do not match", 400)

    try:
        db.execute(
            "UPDATE users SET password = :password1 WHERE username = '"
            + db.execute(
                "SELECT username FROM users WHERE id = (?)", (user_id,)
            ).fetchone()[0]
            + "' AND password = :password2",
            {"password1": new_password, "password2": old_password},
        )
        db.commit()
    except Error as e:
        return (repr(e), 400)

    change_password_successful = db.execute(
        "SELECT id FROM users WHERE username = :original_username AND password = :new_password",
        {"original_username": original_username, "new_password": new_password},
    ).fetchone()

    return ("Success (2/2)", 200) if change_password_successful else ("Failure", 400)
