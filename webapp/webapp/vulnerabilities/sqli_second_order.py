import uuid
from flask import Blueprint, request, session
from sqlalchemy import text
from .. import database
from .. import secrets
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli2", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli2"
)
username_to_exploit = "username_to_exploit_for_sqli2"
user_id_for_registered_account = "user_id_for_registered_account_for_sqli2"


@bp.route("/get_username", methods=["GET"])
def get_username_to_exploit():
    connection = database.get_connection()
    transaction = connection.begin()
    username = str(uuid.uuid4()).replace("-", "")
    password = str(uuid.uuid4()).replace("-", "")

    try:
        query = text(
            "INSERT INTO sqli2_users (username, password) VALUES (:username, :password)"
        )
        connection.execute(query, username=username, password=password)
        transaction.commit()
    except:
        transaction.rollback()
        return ("Failed to generate username", 400)

    session.pop(username_to_exploit, None)
    session[username_to_exploit] = username
    return username


@bp.route("/register", methods=["POST"])
def register():
    connection = database.get_connection()
    transaction = connection.begin()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure: fields can not be empty", 401)

    try:
        query = text(
            "INSERT INTO sqli2_users (username, password) VALUES (:username, :password)"
        )
        connection.execute(query, username=username, password=password)
        transaction.commit()
    except:
        transaction.rollback()
        return ("Failed to create user", 400)

    query = text(
        "SELECT id FROM sqli2_users WHERE username = :username AND password = :password"
    )
    results = connection.execute(query, username=username, password=password)
    user_id = results.fetchone()

    session.pop(user_id_for_registered_account, None)
    session[user_id_for_registered_account] = str(user_id[0])
    return ("Success (1/2)", 200)


@bp.route("/change_password", methods=["POST"])
def change_password():
    connection = database.get_connection()
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
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password1")

    query = text("SELECT username, password FROM sqli2_users WHERE id = :id")
    results = connection.execute(query, id=user_id)
    values = results.fetchone()
    username_from_database = values[0]
    password_from_database = values[1]

    if not old_password or not new_password:
        return ("Failure: fields can not be empty", 401)
    if password_from_database != old_password:
        return ("Failure: incorrect current password", 401)
    if new_password != request.form.get("new_password2"):
        return ("Failure: passwords do not match", 400)

    transaction = connection.begin()
    try:
        query = text(
            f"UPDATE sqli2_users SET password = :new_password WHERE username = '{username_from_database}' AND password = :old_password"
        )

        connection.execute(query, new_password=new_password, old_password=old_password)
        transaction.commit()
    except:
        transaction.rollback()
        return ("Failed to change password", 400)

    query = text(
        "SELECT id FROM sqli2_users WHERE username = :username AND password = :password"
    )
    results = connection.execute(
        query, username=original_username, password=new_password
    )
    change_password_successful = results.fetchone()

    return (f"Success (2/2) - passphrase: {secrets.PASSPHRASE['sqli2']}", 200) if change_password_successful else ("Failure", 400)
