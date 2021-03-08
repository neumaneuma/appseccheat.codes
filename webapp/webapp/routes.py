from flask import Blueprint, render_template

bp = Blueprint("routes", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# TODO remove this and make it a command line
@bp.route("/reset")
def reset_database():
    from . import database
    database.reset_database()

    return "reset"
