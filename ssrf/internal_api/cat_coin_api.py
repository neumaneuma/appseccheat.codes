from flask import Blueprint
from datetime import datetime
import random


bp = Blueprint("ssrf-local-file-inclusion", __name__, url_prefix="/")


@bp.route("get_cat_coin_price_v2/", methods=["GET"])
def get_cat_coin_price_v2():
    return f"Price at {datetime.now().time()} - ${random.random() * 100}"

@bp.route("get_cat_coin_price_v1/", methods=["GET"])
def get_cat_coin_price_v1():
    return f"Price at {datetime.now().time()} - ${random.random() * 100}"