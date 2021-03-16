from flask import Blueprint, render_template

bp = Blueprint("routes", __name__)


# TODO remove this and make it a command line
@bp.route("/reset")
def reset_database():
    from . import database

    database.reset_database()

    return "reset"


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/sqli1", methods=["GET"])
def sqli1():
    return render_template("challenge.html")
