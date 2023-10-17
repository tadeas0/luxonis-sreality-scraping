import psycopg
import scrapy
from items import EstateItem


class PostgresPipeline:
    collection_name = "Estate"

    db_client: psycopg.Connection

    def __init__(self, postgres_url: str):
        self.postgres_url = postgres_url

    @classmethod
    def from_crawler(cls, crawler: scrapy.Spider):
        return cls(
            postgres_url=crawler.settings.get("POSTGRES_URL"),
        )

    def open_spider(self, spider: scrapy.Spider):
        self.db_client = psycopg.connect(conninfo=self.postgres_url)
        with self.db_client.cursor() as c:
            c.execute("""
                        CREATE TABLE IF NOT EXISTS estate (
                            id serial PRIMARY KEY,
                            name varchar(255) NOT NULL,
                            sreality_id bigint UNIQUE NOT NULL
                        );
                      """)
            c.execute("""
                        CREATE TABLE IF NOT EXISTS image (
                            id serial PRIMARY KEY,
                            url varchar(255) NOT NULL,
                            estate_id int NOT NULL,
                            FOREIGN KEY (estate_id)
                                REFERENCES estate (id)
                        );
                      """)

    def close_spider(self, spider: scrapy.Spider):
        self.db_client.close()

    def process_item(self, item: EstateItem, spider: scrapy.Spider):
        with self.db_client.cursor() as c:
            try:
                res = c.execute("""
                                INSERT INTO estate (name, sreality_id)
                                VALUES (%s, %s) RETURNING id;
                                """,
                                (item["name"], item["sreality_id"])).fetchone()

            # Estate with this sreality_id is already present in the DB
            except psycopg.IntegrityError:
                self.db_client.rollback()
                return item

            if res is not None:
                estate_id = res[0]

                image_tuples = [(i, estate_id) for i in item["image_urls"]]
                c.executemany("""
                                INSERT INTO image (url, estate_id)
                                VALUES (%s, %s)
                            """, image_tuples)
                self.db_client.commit()
            else:
                self.db_client.rollback()
        return item
