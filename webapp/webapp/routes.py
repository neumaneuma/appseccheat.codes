from flask import Blueprint, render_template, url_for, request, flash, redirect
from urllib.parse import urlparse
from . import html_builder
from . import secrets

bp = Blueprint("routes", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", collapsible_is_present=False)


@bp.route("/faq/", methods=["GET"])
def faq():
    return render_template("faq.html", collapsible_is_present=False)


def should_show_introduction(routes):
    refer = request.headers.get("referer")
    if not refer:
        return True
    refer_path = urlparse(refer).path
    return refer_path not in routes


@bp.route("/sqli1/", methods=["GET", "POST"])
def sqli1():
    routes_to_not_show_introduction_for = {url_for("routes.sqli2")}

    headers = html_builder.build_headers(
        "Challenge #1: SQLi login bypass", "What is SQL injection?", "Congratulations on solving the first challenge!"
    )
    challenge_links = {"prev": "", "next": url_for("routes.sqli2")}

    if request.method == "GET":
        return render_template(
            "sqli/sqli1_challenge.html",
            headers=headers,
            gh_links=html_builder.SQLI1_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.sqli1"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != secrets.PASSPHRASE["sqli1"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "sqli/sqli1_answer.html",
        headers=headers,
        gh_links=html_builder.SQLI1_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/sqli2/", methods=["GET", "POST"])
def sqli2():
    routes_to_not_show_introduction_for = {url_for("routes.sqli1")}

    headers = html_builder.build_headers(
        "Challenge #2: SQLi second order", "What is SQL injection?", "Congratulations on solving the second challenge!"
    )
    challenge_links = {"prev": url_for("routes.sqli1"), "next": url_for("routes.ssrf1")}

    if request.method == "GET":
        return render_template(
            "sqli/sqli2_challenge.html",
            headers=headers,
            gh_links=html_builder.SQLI2_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.sqli2"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != secrets.PASSPHRASE["sqli2"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "sqli/sqli2_answer.html",
        headers=headers,
        gh_links=html_builder.SQLI2_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/ssrf1/", methods=["GET", "POST"])
def ssrf1():
    routes_to_not_show_introduction_for = {url_for("routes.ssrf2")}

    headers = html_builder.build_headers(
        "Challenge #3: SSRF bypass webhook", "What is SSRF?", "Congratulations on solving the third challenge!"
    )
    challenge_links = {"prev": url_for("routes.sqli2"), "next": url_for("routes.ssrf2")}

    if request.method == "GET":
        return render_template(
            "ssrf/ssrf1_challenge.html",
            headers=headers,
            gh_links=html_builder.SSRF1_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.ssrf1"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != secrets.PASSPHRASE["ssrf1"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "ssrf/ssrf1_answer.html",
        headers=headers,
        gh_links=html_builder.SSRF1_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/ssrf2/", methods=["GET", "POST"])
def ssrf2():

    routes_to_not_show_introduction_for = {url_for("routes.ssrf1")}

    headers = html_builder.build_headers(
        "Challenge #4: SSRF local file inclusion", "What is SSRF?", "Congratulations on solving the fourth challenge!"
    )
    challenge_links = {"prev": url_for("routes.ssrf1"), "next": ""}

    if request.method == "GET":
        return render_template(
            "ssrf/ssrf2_challenge.html",
            headers=headers,
            gh_links=html_builder.SSRF2_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.ssrf2"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != secrets.PASSPHRASE["ssrf2"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "ssrf/ssrf2_answer.html",
        headers=headers,
        gh_links=html_builder.SSRF2_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )
