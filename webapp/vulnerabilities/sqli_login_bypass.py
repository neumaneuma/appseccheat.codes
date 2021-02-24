from webapp import db as database
from flask import Blueprint, request
from webapp.vulnerabilities import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_sqli1", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/sqli1"
)


@bp.route("/login", methods=["POST"])
def login():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = db.execute(
        f"SELECT * FROM users WHERE password = '{password}' AND username = '{username}'"
    ).fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)
