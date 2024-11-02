from admin_panel import bp as admin_panel_bp
from cat_coin_api import bp as cat_coin_api_bp
from flask import Flask, render_template

# Gunicorn requires the exposed flask app to be called `application`
application = Flask(__name__)
application.register_blueprint(admin_panel_bp)
application.register_blueprint(cat_coin_api_bp)


@application.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    application.run(host="0.0.0.0")
