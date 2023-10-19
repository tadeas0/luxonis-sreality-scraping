import schedule
import time
from subprocess import call
from settings import SCRAPING_INTERVAL_MINUTES


def run_spider():
    call(['scrapy', 'crawl', 'sreality'])


if __name__ == "__main__":
    schedule.every(SCRAPING_INTERVAL_MINUTES).minutes.do(run_spider)
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
