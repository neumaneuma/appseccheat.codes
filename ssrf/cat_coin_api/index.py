from datetime import datetime
import random
from flask import Flask

app = Flask(__name__)


@app.route("/get_cat_coin_price/", methods=["GET"])
def get_cat_coin_price():
    return f"Price at {datetime.now().time()} - ${random.random() * 100}"
