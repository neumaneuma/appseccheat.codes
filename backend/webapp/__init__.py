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

        from .vulnerabilities import sqli-login-bypass as v_sqli-login-bypass
        from .vulnerabilities import sqli_second_order as v_sqli-second-order
        from .vulnerabilities import ssrf_webhook as v_ssrf-bypass-webhook
        from .vulnerabilities import ssrf_lfi as v_ssrf-local-file-inclusion
        from .patches import sqli-login-bypass as p_sqli-login-bypass
        from .patches import sqli_second_order as p_sqli-second-order
        from .patches import ssrf_webhook as p_ssrf-bypass-webhook
        from .patches import ssrf_lfi as p_ssrf-local-file-inclusion
        from . import routes

        app.register_blueprint(v_sqli-login-bypass.bp)
        app.register_blueprint(v_sqli-second-order.bp)
        app.register_blueprint(v_ssrf-bypass-webhook.bp)
        app.register_blueprint(v_ssrf-local-file-inclusion.bp)
        app.register_blueprint(p_sqli-login-bypass.bp)
        app.register_blueprint(p_sqli-second-order.bp)
        app.register_blueprint(p_ssrf-bypass-webhook.bp)
        app.register_blueprint(p_ssrf-local-file-inclusion.bp)
        app.register_blueprint(routes.bp)
        app.register_blueprint(database.bp)

        return app
