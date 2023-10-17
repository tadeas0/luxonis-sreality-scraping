import psycopg
from flask import g
from settings import POSTGRES_URL


class MissingEnvVarException(Exception):
    pass


def get_db():
    if "db" not in g:
        if not POSTGRES_URL:
            raise MissingEnvVarException("missing POSTGRES_URL")

        conn = psycopg.connect(conninfo=POSTGRES_URL)
        g.db = conn
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
