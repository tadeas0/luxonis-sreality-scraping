import psycopg
from estate_db.model import EstateCreationDTO, Estate, Image
import estate_db.queries as queries


class DBClient:
    def __init__(self, postgres_url: str) -> None:
        self.postgres_url = postgres_url
        self.connection = None

    def _get_connection(self) -> psycopg.Connection:
        if self.connection is None:
            self.connection = psycopg.connect(conninfo=self.postgres_url)
        return self.connection

    def init_db(self) -> None:
        conn = self._get_connection()
        with conn.cursor() as c:
            c.execute(queries.create_estate_table)
            c.execute(queries.create_image_table)

    def close(self) -> None:
        self._get_connection().close()

    def insert_estate(self, item: EstateCreationDTO) -> None:
        conn = self._get_connection()
        with conn.cursor() as c:
            try:
                res = c.execute(
                    queries.insert_estate,
                    (item.name, item.sreality_id)
                ).fetchone()

            # Estate with this sreality_id is already present in the DB
            except psycopg.IntegrityError:
                conn.rollback()
                return

            if res is not None:
                estate_id = res[0]

                image_tuples = [(i.url, estate_id) for i in item.images]
                c.executemany(queries.insert_image, image_tuples)
                conn.commit()
            else:
                conn.rollback()

    def get_estates(
        self,
        take: int | None = None,
        skip: int | None = None
    ) -> list[Estate]:
        conn = self._get_connection()
        res = conn.execute(queries.select_estates_images, (take, skip))

        if res is None:
            return []

        estate_dict: dict[str, Estate] = dict()
        for i in res.fetchall():
            estate_id, sreality_id, image_id, estate_name, image_url = i
            new_image = Image(image_id, image_url)
            if estate_id in estate_dict:
                estate_dict[estate_id].images.append(new_image)
            else:
                estate_dict[estate_id] = Estate(
                    estate_id,
                    sreality_id,
                    estate_name,
                    [new_image]
                )

        return list(estate_dict.values())

    def get_estate_count(self) -> int:
        conn = self._get_connection()
        res = conn.execute(queries.select_estate_count)

        if res is None:
            return 0

        count = res.fetchone()

        if count is None:
            return 0

        return count[0]
