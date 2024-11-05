from flask import Blueprint

bp = Blueprint("ssrf1", __name__, url_prefix="/")

PASSWORD_RESET = (
    "E0304F61-0E09-4200-8086-AC2C6546F56F-835A6D48-E659-4F55-8730-9636A9F55E92"
)


@bp.route("reset_admin_password/", methods=["GET"])
def simulate_reset_admin_password():
    return f"Administrator password reset to: {PASSWORD_RESET}"
