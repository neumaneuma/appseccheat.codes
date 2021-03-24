from flask import Blueprint, render_template, url_for, request
from urllib.parse import urlparse
from . import html_builder

bp = Blueprint("routes", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")


def should_show_introduction(routes):
    refer = request.headers.get("referer")
    refer_path = urlparse(refer).path
    return refer_path not in routes


@bp.route("/sqli1", methods=["GET"])
def sqli1():
    routes_to_not_show_introduction_for = {url_for("routes.sqli2")}

    headers = html_builder.build_headers(
        "Challenge #1: SQLi login bypass", "What is SQL injection?"
    )
    challenge_links = {"prev": "", "next": url_for("routes.sqli2")}

    return render_template(
        "sqli1_challenge.html",
        headers=headers,
        gh_links=html_builder.SQLI1_LINKS,
        challenge_links=challenge_links,
        should_show_introduction=should_show_introduction(
            routes_to_not_show_introduction_for),
        current_link=url_for("routes.sqli1")
    )


@bp.route("/sqli2", methods=["GET"])
def sqli2():
    routes_to_not_show_introduction_for = {url_for("routes.sqli1")}

    headers = html_builder.build_headers(
        "Challenge #2: SQLi second order", "What is SQL injection?"
    )
    challenge_links = {"prev": url_for("routes.sqli1"), "next": ""}
    return render_template(
        "sqli2_challenge.html",
        headers=headers,
        gh_links=html_builder.SQLI2_LINKS,
        challenge_links=challenge_links,
        should_show_introduction=should_show_introduction(
            routes_to_not_show_introduction_for),
        current_link=url_for("routes.sqli2")
    )
