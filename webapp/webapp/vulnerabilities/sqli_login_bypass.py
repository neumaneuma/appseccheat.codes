from flask import Blueprint, request
from .. import database
from .. import secrets
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli1", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli1"
)


@bp.route("/login", methods=["POST"])
def login():
    connection = database.get_connection()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure: fields can not be empty", 401)

    query = f"SELECT * FROM sqli1_users WHERE password = '{password}' AND username = '{username}'"
    results = connection.execute(query)
    user_valid = results.fetchone()

    return (f"Success - passphrase: {secrets.PASSPHRASE['sqli1']}", 200) if user_valid else ("Failure", 401)
