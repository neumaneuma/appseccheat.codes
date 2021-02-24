from webapp import db as database
from sqlite3.dbapi2 import Error
from flask import Blueprint, request
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "sqli_second_order", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli2"
)


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
        # to do need to decide how to handle errors
        return (repr(e), 400)
    return ("Success (1/2)", 200)


@bp.route("/change_password", methods=["POST"])
def change_password():
    db = database.get_db()
    original_username = "administrator"
    user_id = "2"
    old_password = request.form["old_password"]
    new_password = request.form["new_password1"]
    if new_password != request.form["new_password2"]:
        return ("Passwords do not match", 400)

    try:
        db.execute(
            "UPDATE users SET password = :password1 WHERE username = '"
            + db.execute(
                "SELECT username FROM users WHERE id = (?)", (user_id)
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

    return ("Success", 200) if change_password_successful else ("Failure", 400)
