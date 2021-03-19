from flask import Blueprint, render_template, url_for
from . import html_builder

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
    headers = html_builder.build_headers("Challenge #1: SQLi login bypass", "What is SQL injection?")
    challenges = {'prev': None, "next": url_for("routes.sqli2")}
    return render_template(
        "sqli1_challenge.html", headers=headers, links=html_builder.SQLI1_LINKS
    )


@bp.route("/sqli2", methods=["GET"])
def sqli2():
    headers = html_builder.build_headers("Challenge #2: SQLi second order", "What is SQL injection?")
    return render_template(
        "sqli2_challenge.html", headers=headers, links=html_builder.SQLI2_LINKS
    )
