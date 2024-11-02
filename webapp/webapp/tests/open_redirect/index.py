from flask import Flask, redirect

app = Flask(__name__)


# http://127.0.0.1:12302/permanent/
@app.route("/permanent/", methods=["GET"])
def permanent():
    return redirect("http://127.0.0.1:12300", 301)


# http://127.0.0.1:12302/temporary/
@app.route("/temporary/", methods=["GET"])
def temporary():
    return redirect("http://127.0.0.1:12300", 307)
