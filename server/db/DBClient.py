import psycopg
import db.queries as queries
from dataclasses import dataclass


@dataclass
class Estate:
    id: int
    name: str
    image_urls: list[str]


class DBClient:
    def __init__(self, postgres_url: str):
        self.postgres_url = postgres_url
        self.connection = None

    def _get_connection(self):
        if self.connection is None:
            self.connection = psycopg.connect(conninfo=self.postgres_url)
        return self.connection

    def get_estates(self):
        conn = self._get_connection()
        res = conn.execute(queries.select_estates_images)

        if res is None:
            return []

        estate_dict: dict[str, Estate] = dict()
        for i in res.fetchall():
            id, name, url = i
            if id in estate_dict:
                estate_dict[id].image_urls.append(url)
            else:
                estate_dict[id] = Estate(id, name, [url])

        return list(estate_dict.values())

    def close(self):
        self._get_connection().close()
