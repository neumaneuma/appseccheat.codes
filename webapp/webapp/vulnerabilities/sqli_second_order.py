import uuid
from flask import Blueprint, request, session
import mysql.connector
from .. import database
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli2", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli2"
)
username_to_exploit = "username_to_exploit_for_sqli2"
user_id_for_registered_account = "user_id_for_registered_account_for_sqli2"


@bp.route("/get_username", methods=["GET"])
def get_username_to_exploit():
    connection = database.get_connection()
    cursor = connection.cursor()
    username = str(uuid.uuid4()).replace("-", "")
    password = str(uuid.uuid4()).replace("-", "")

    cursor.execute(
        "INSERT INTO sqli2_users (username, password) VALUES (%s, %s)",
        (username, password),
    )
    connection.commit()

    session.pop(username_to_exploit, None)
    session[username_to_exploit] = username
    return username


@bp.route("/register", methods=["POST"])
def register():
    connection = database.get_connection()
    cursor = connection.cursor()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure: fields can not be empty", 401)

    try:
        cursor.execute(
            "INSERT INTO sqli2_users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        connection.commit()
    except mysql.connector.Error as e:
        return (repr(e), 400)

    cursor.execute(
        "SELECT id FROM sqli2_users WHERE username = %s AND password = %s",
        (username, password),
    )
    user_id = cursor.fetchone()

    session.pop(user_id_for_registered_account, None)
    session[user_id_for_registered_account] = str(user_id[0])
    return ("Success (1/2)", 200)


@bp.route("/change_password", methods=["POST"])
def change_password():
    connection = database.get_connection()
    cursor = connection.cursor()
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

    cursor.execute(
        "SELECT username, password FROM sqli2_users WHERE id = %s", (user_id,)
    )
    values = cursor.fetchone()
    username = values[0]
    password = values[1]

    if not old_password or not new_password:
        return ("Failure: fields can not be empty", 401)
    if password != old_password:
        return ("Failure: incorrect current password", 401)
    if new_password != request.form.get("new_password2"):
        return ("Failure: passwords do not match", 400)

    try:
        query = f"UPDATE sqli2_users SET password = %s WHERE username = '{username}' AND password = %s"
        cursor.execute(query, (new_password, old_password))
        connection.commit()
    except mysql.connector.Error as e:
        return (repr(e), 400)

    cursor.execute(
        "SELECT id FROM sqli2_users WHERE username = %s AND password = %s",
        (original_username, new_password),
    )
    change_password_successful = cursor.fetchone()

    return ("Success (2/2)", 200) if change_password_successful else ("Failure", 400)
