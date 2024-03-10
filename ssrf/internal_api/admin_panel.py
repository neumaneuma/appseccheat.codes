from flask import Blueprint

bp = Blueprint("ssrf-bypass-webhook", __name__, url_prefix="/")


@bp.route("reset_admin_password/", methods=["POST", "GET"])
def reset_admin_password():
    return "Administrator password reset to: admin"
