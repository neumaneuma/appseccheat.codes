import os
from flask import Flask
from . import db as database

def init_app():
    # app = Flask(__name__, instance_relative_config=False)
    app = Flask(__name__, instance_relative_config=True)
    # to do the tutorial hours following had instance relative configs set toFalse
    app.config.from_object("config.DevConfig")
    # app.config.from_object("config.ProdConfig")


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    database.init_app(app)
    
    
    # @app.route("/")
    # def index():
    #     return app.send_static_file("index.html")

    with app.app_context():
        from .vulnerabilities import sqli_login_bypass as v_sqli1
        from .vulnerabilities import sqli_second_order as v_sqli2
        from .patches import sqli_login_bypass as p_sqli1
        from .patches import sqli_second_order as p_sqli2

        app.register_blueprint(v_sqli1.bp)
        app.register_blueprint(v_sqli2.bp)
        app.register_blueprint(p_sqli1.bp)
        app.register_blueprint(p_sqli2.bp)

        return app
