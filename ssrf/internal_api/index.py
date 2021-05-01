from flask import Flask, render_template
from .admin_panel import bp as admin_panel_bp
from .cat_coin_api import bp as cat_coin_api_bp

app = Flask(__name__)
app.register_blueprint(admin_panel_bp)
app.register_blueprint(cat_coin_api_bp)



@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
