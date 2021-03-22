from flask import Blueprint, request
from .. import database
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli1", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli1"
)


@bp.route("/login", methods=["POST"])
def login():
    engine = database.get_engine()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure: fields can not be empty", 401)

    results = engine.execute(
        f"SELECT * FROM sqli1_users WHERE password = '{password}' AND username = '{username}'"
    )
    user_valid = results.fetchone()

    return ("Success", 200) if user_valid else ("Failure", 401)
