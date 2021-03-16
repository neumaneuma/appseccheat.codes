from flask import request, Blueprint
from .. import database
from . import PATCHES_PREFIX

bp = Blueprint("patches_sqli1", __name__, url_prefix=f"{PATCHES_PREFIX}/sqli1")


@bp.route("/login", methods=["POST"])
def login():
    connection = database.get_connection()
    cursor = connection.cursor()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return ("Failure", 401)

    cursor.execute(f"SELECT * FROM sqli1_users WHERE password = %s AND username = %s", (username, password))
    user_valid = cursor.fetchone()

    return ("Success", 200) if user_valid else ("Failure", 401)
