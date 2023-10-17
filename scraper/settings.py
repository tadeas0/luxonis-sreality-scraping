import os

BOT_NAME = "scraper"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
ITEM_PIPELINES = {
    "pipelines.PostgresPipeline": 300,
}
POSTGRES_URL = os.environ.get("POSTGRES_URL")
