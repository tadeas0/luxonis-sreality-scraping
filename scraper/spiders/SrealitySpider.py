import scrapy

from items import EstateItem


class SrealitySpider(scrapy.Spider):
    name = "sreality"
    start_urls = [
        (
            "https://www.sreality.cz/api/cs/v2/estates?"
            "category_main_cb=1&"
            "category_type_cb=1&"
            "page=1&per_page=500"
        )
    ]

    def parse(self, response):
        data = response.json()

        for estate in data["_embedded"]["estates"]:
            image_urls = [i["href"] for i in estate["_links"]["images"]]
            yield EstateItem(name=estate["name"], image_urls=image_urls)
