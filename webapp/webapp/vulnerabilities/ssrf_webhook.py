import requests
from flask import Blueprint, request
from .. import secrets
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_ssrf1", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/ssrf1"
)


@bp.route("/submit_webhook", methods=["POST"])
def submit_webhook():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 401)
    if custom_url.startswith("http://127.0.0.1") or custom_url.startswith(
        "http://localhost"
    ):
        return "Docker container in use - use admin_panel as hostname to access admin functionality."
    if custom_url.startswith("http://admin_panel") and not custom_url.startswith(
        "http://admin_panel:8484"
    ):
        return "Incorrect port. Use 8484 instead."
    r = requests.post(custom_url)
    response_body = r.text[:1000]

    return (
        (f"{response_body}\n\nSuccess - passphrase: {secrets.PASSPHRASE['ssrf1']}", 200)
        if was_successful_ssrf_attack(custom_url)
        else (f"{response_body}...\n\nFailure", 401)
    )


def was_successful_ssrf_attack(url):
    successful_url = "http://admin_panel:8484/reset_admin_password"
    return url == successful_url or url == successful_url + "/"
