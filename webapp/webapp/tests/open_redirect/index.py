from flask import Flask
from flask import redirect

app = Flask(__name__)


# http://127.0.0.1:8485/permanent/
@app.route("/permanent/", methods=["GET"])
def permanent():
    return redirect("http://127.0.0.1:5000", 301)


# http://127.0.0.1:8485/temporary/
@app.route("/temporary/", methods=["GET"])
def temporary():
    return redirect("http://127.0.0.1:5000", 307)
