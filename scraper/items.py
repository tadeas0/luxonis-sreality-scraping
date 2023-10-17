import scrapy


class EstateItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
