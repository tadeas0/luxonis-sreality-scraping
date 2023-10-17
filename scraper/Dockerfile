FROM python:3.12

RUN mkdir /scraper
WORKDIR /scraper
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["scrapy", "crawl", "sreality"]