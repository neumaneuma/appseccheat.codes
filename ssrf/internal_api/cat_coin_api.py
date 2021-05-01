from flask import Blueprint
from datetime import datetime
import random


bp = Blueprint("ssrf2", __name__, url_prefix="/")


@bp.route("get_cat_coin_price/", methods=["GET"])
def get_cat_coin_price():
    return f"Price at {datetime.now().time()} - ${random.random() * 100}"
