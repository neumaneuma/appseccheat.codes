import os
from flask import Flask
from webapp import db as database
from webapp.vulnerabilities import sqli_login_bypass as vulnerabilities_sqli1
from webapp.vulnerabilities import sqli_second_order as vulnerabilities_sqli2
from webapp.patches import sqli_login_bypass as patches_sqli1
from webapp.patches import sqli_second_order as patches_sqli2

app = Flask(__name__)
app.register_blueprint(vulnerabilities_sqli1.bp)
app.register_blueprint(vulnerabilities_sqli2.bp)
app.register_blueprint(patches_sqli1.bp)
app.register_blueprint(patches_sqli2.bp)
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
