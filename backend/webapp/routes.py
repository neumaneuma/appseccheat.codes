from flask import Blueprint, render_template, url_for, request, flash, redirect
from urllib.parse import urlparse
from . import html_builder
from .. import local_flags

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


@bp.route("/sqli-login-bypass/", methods=["GET", "POST"])
def sqli-login-bypass():
    routes_to_not_show_introduction_for = {url_for("routes.sqli-second-order")}

    headers = html_builder.build_headers(
        "Challenge #1: SQLi login bypass", "What is SQL injection?", "Congratulations on solving the first challenge!"
    )
    challenge_links = {"prev": "", "next": url_for("routes.sqli-second-order")}

    if request.method == "GET":
        return render_template(
            "sqli/sqli-login-bypass_challenge.html",
            headers=headers,
            gh_links=html_builder.sqli-login-bypass_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.sqli-login-bypass"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != local_flags.PASSPHRASE["sqli-login-bypass"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "sqli/sqli-login-bypass_answer.html",
        headers=headers,
        gh_links=html_builder.sqli-login-bypass_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/sqli-second-order/", methods=["GET", "POST"])
def sqli-second-order():
    routes_to_not_show_introduction_for = {url_for("routes.sqli-login-bypass")}

    headers = html_builder.build_headers(
        "Challenge #2: SQLi second order", "What is SQL injection?", "Congratulations on solving the second challenge!"
    )
    challenge_links = {"prev": url_for("routes.sqli-login-bypass"), "next": url_for("routes.ssrf-bypass-webhook")}

    if request.method == "GET":
        return render_template(
            "sqli/sqli-second-order_challenge.html",
            headers=headers,
            gh_links=html_builder.sqli-second-order_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.sqli-second-order"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != local_flags.PASSPHRASE["sqli-second-order"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "sqli/sqli-second-order_answer.html",
        headers=headers,
        gh_links=html_builder.sqli-second-order_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/ssrf-bypass-webhook/", methods=["GET", "POST"])
def ssrf-bypass-webhook():
    routes_to_not_show_introduction_for = {url_for("routes.ssrf-local-file-inclusion")}

    headers = html_builder.build_headers(
        "Challenge #3: SSRF bypass webhook", "What is SSRF?", "Congratulations on solving the third challenge!"
    )
    challenge_links = {"prev": url_for("routes.sqli-second-order"), "next": url_for("routes.ssrf-local-file-inclusion")}

    if request.method == "GET":
        return render_template(
            "ssrf/ssrf-bypass-webhook_challenge.html",
            headers=headers,
            gh_links=html_builder.ssrf-bypass-webhook_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.ssrf-bypass-webhook"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != local_flags.PASSPHRASE["ssrf-bypass-webhook"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "ssrf/ssrf-bypass-webhook_answer.html",
        headers=headers,
        gh_links=html_builder.ssrf-bypass-webhook_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )


@bp.route("/ssrf-local-file-inclusion/", methods=["GET", "POST"])
def ssrf-local-file-inclusion():

    routes_to_not_show_introduction_for = {url_for("routes.ssrf-bypass-webhook")}

    headers = html_builder.build_headers(
        "Challenge #4: SSRF local file inclusion", "What is SSRF?", "Congratulations on solving the fourth challenge!"
    )
    challenge_links = {"prev": url_for("routes.ssrf-bypass-webhook"), "next": ""}

    if request.method == "GET":
        return render_template(
            "ssrf/ssrf-local-file-inclusion_challenge.html",
            headers=headers,
            gh_links=html_builder.ssrf-local-file-inclusion_LINKS,
            challenge_links=challenge_links,
            should_show_introduction=should_show_introduction(
                routes_to_not_show_introduction_for),
            current_link=url_for("routes.ssrf-local-file-inclusion"),
            collapsible_is_present=True
        )

    passphrase = request.form.get("passphrase")
    if passphrase != local_flags.PASSPHRASE["ssrf-local-file-inclusion"]:
        flash("Passphrase incorrect", "passphrase")
        return redirect(f"{request.url}#passphrase_form")

    return render_template(
        "ssrf/ssrf-local-file-inclusion_answer.html",
        headers=headers,
        gh_links=html_builder.ssrf-local-file-inclusion_LINKS,
        challenge_links=challenge_links,
        collapsible_is_present=False
    )
