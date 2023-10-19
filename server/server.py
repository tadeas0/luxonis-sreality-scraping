from flask import Flask
import logging
import settings


def setup_logging():
    logger = logging.getLogger(settings.DEFAULT_LOGGER)

    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def create_app():
    logger = setup_logging()

    app = Flask(__name__)

    from db_helpers import init_app
    init_app(app)

    from estates_bp import estates_bp
    app.register_blueprint(estates_bp)

    logger.info("Application initialized")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
