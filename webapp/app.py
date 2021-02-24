from flask import Flask
from flask import request
import os
from . import db as database
from .vulnerabilities import sqli1 as a
from .patches import sqli1 as b
from .patches import sqli2 as d
from .vulnerabilities import sqli2 as c

app = Flask(__name__)
app.register_blueprint(a.vulnerability_bp)
app.register_blueprint(b.patch_bp)
app.register_blueprint(c.bp)
app.register_blueprint(d.bp)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

database.init_app(app)


@app.route("/")
def index():
    return app.send_static_file("index.html")
