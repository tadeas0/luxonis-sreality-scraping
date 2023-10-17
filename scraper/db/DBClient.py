import psycopg
from items import EstateItem
import db.queries as queries


class DBClient:
    def __init__(self, postgres_url: str):
        self.postgres_url = postgres_url
        self.connection = None

    def _get_connection(self):
        if self.connection is None:
            self.connection = psycopg.connect(conninfo=self.postgres_url)
        return self.connection

    def init_db(self):
        conn = self._get_connection()
        with conn.cursor() as c:
            c.execute(queries.create_estate_table)
            c.execute(queries.create_image_table)

    def insert_estate(self, item: EstateItem):
        conn = self._get_connection()
        with conn.cursor() as c:
            try:
                res = c.execute(
                    queries.insert_estate,
                    (item["name"], item["sreality_id"])
                ).fetchone()

            # Estate with this sreality_id is already present in the DB
            except psycopg.IntegrityError:
                conn.rollback()
                return item

            if res is not None:
                estate_id = res[0]

                image_tuples = [(i, estate_id) for i in item["image_urls"]]
                c.executemany(queries.insert_image, image_tuples)
                conn.commit()
            else:
                conn.rollback()

    def close(self):
        self._get_connection().close()
