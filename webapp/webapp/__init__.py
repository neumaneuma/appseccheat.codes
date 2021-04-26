from os import environ
import logging
from flask import Flask
from . import database


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    with app.app_context():
        logging.basicConfig(
            filename="main.log",
            format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
            level=logging.DEBUG,
        )
        if environ.get("FLASK_ENV") != "development":
            gunicorn_logger = logging.getLogger("gunicorn.error")
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)

        database.init_connection(app)

        from .vulnerabilities import sqli_login_bypass as v_sqli1
        from .vulnerabilities import sqli_second_order as v_sqli2
        from .vulnerabilities import ssrf_webhook as v_ssrf1
        from .patches import sqli_login_bypass as p_sqli1
        from .patches import sqli_second_order as p_sqli2
        from .patches import ssrf_webhook as p_ssrf1
        from . import routes

        app.register_blueprint(v_sqli1.bp)
        app.register_blueprint(v_sqli2.bp)
        app.register_blueprint(v_ssrf1.bp)
        app.register_blueprint(p_sqli1.bp)
        app.register_blueprint(p_sqli2.bp)
        app.register_blueprint(p_ssrf1.bp)
        app.register_blueprint(routes.bp)
        app.register_blueprint(database.bp)

        return app
