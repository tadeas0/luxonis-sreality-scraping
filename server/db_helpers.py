from flask import Flask, g
from settings import POSTGRES_URL
from estate_db.DBClient import DBClient


class MissingEnvVarException(Exception):
    pass


def get_db():
    if "db" not in g:
        if not POSTGRES_URL:
            raise MissingEnvVarException("missing POSTGRES_URL")

        db = DBClient(POSTGRES_URL)
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
