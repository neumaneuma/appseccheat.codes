from flask import Flask, Blueprint

bp = Blueprint("ssrf2", __name__, url_prefix="api")
