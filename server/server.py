from flask import Flask


def create_app():
    app = Flask(__name__)

    from db_helpers import init_app
    init_app(app)

    from estates_bp import estates_bp
    app.register_blueprint(estates_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
