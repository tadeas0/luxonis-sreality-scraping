import scrapy
from items import EstateItem
from estate_db.DBClient import DBClient
from estate_db.model import ImageCreationDTO, EstateCreationDTO


class PostgresPipeline:
    """Pipeline responsible for saving scraped items to Postgres database"""

    def __init__(self, postgres_url: str):
        self.postgres_url = postgres_url
        self.db_client = DBClient(self.postgres_url)

    @classmethod
    def from_crawler(cls, crawler: scrapy.Spider):
        return cls(
            postgres_url=crawler.settings.get("POSTGRES_URL"),
        )

    def open_spider(self, spider: scrapy.Spider):
        self.db_client.init_db()

    def close_spider(self, spider: scrapy.Spider):
        self.db_client.close()

    def process_item(self, item: EstateItem, spider: scrapy.Spider):
        images = [ImageCreationDTO(i) for i in item["image_urls"]]
        estate = EstateCreationDTO(
            item["sreality_id"],
            item["name"],
            images
        )
        self.db_client.insert_estate(estate)
        return item
