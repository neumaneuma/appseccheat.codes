from flask import request
from webapp import db as database
from flask import Blueprint


patch_bp = Blueprint('patch_sqli1', __name__, url_prefix='/patches')

@patch_bp.route("/login", methods=["POST"])
def login():
    db = database.get_db()
    username = request.form["username"]
    password = request.form["password"]
    user_valid = db.execute("SELECT id FROM users WHERE password = :password AND username = :username", {"password" :password, "username" :username}).fetchone()
    return ("Success", 200) if user_valid else ("Failure", 401)
