from webapp import db as database
from flask import (
    Blueprint, request
)

vulnerability_bp = Blueprint('vulnerability_sqli1', __name__, url_prefix='/vulnerabilities')


@vulnerability_bp.route("/login", methods=["POST"])
def login():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = db.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'").fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)
