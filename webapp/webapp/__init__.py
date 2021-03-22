from flask import Flask
from . import database


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    with app.app_context():
        database.init_connection(app)

    with app.app_context():
        from .vulnerabilities import sqli_login_bypass as v_sqli1
        from .vulnerabilities import sqli_second_order as v_sqli2
        from .patches import sqli_login_bypass as p_sqli1
        from .patches import sqli_second_order as p_sqli2
        from . import routes

        app.register_blueprint(v_sqli1.bp)
        app.register_blueprint(v_sqli2.bp)
        app.register_blueprint(p_sqli1.bp)
        app.register_blueprint(p_sqli2.bp)
        app.register_blueprint(routes.bp)

        return app
