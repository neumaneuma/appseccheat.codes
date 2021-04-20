from flask import Flask, render_template

app = Flask(__name__)


@app.route("/reset_admin_password", methods=["POST", "GET"])
def reset_admin_password():
    return "Administrator password reset to: admin"


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
