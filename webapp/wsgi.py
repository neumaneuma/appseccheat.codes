"""Application entry point."""
from webapp import init_app

# Gunicorn requires the exposed flask app to be called `application`
application = init_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0")
