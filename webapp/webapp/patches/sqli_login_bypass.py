from sqlalchemy import text
from flask import request, Blueprint
from .. import database
from . import PATCHES_PREFIX

bp = Blueprint("patches_sqli1", __name__, url_prefix=f"{PATCHES_PREFIX}/sqli1")


@bp.route("/login", methods=["POST"])
def login():
    engine = database.get_engine()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure: fields can not be empty", 401)

    query = text(
        f"SELECT * FROM sqli1_users WHERE password = :password AND username = :username"
    )
    results = engine.execute(query, password=password, username=username)
    user_valid = results.fetchone()

    return ("Success", 200) if user_valid else ("Failure", 401)
