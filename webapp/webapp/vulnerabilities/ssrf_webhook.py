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
    requests.post(custom_url)
    return str(custom_url)


    # return (f"Success - passphrase: {secrets.PASSPHRASE['ssrf1']}", 200) if user_valid else ("Failure", 401)
