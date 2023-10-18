FROM python:3.12

RUN mkdir /scraper
WORKDIR /scraper
COPY ./estate_db ./estate_db
RUN pip install ./estate_db
COPY ./scraper/requirements.txt .
RUN pip install -r requirements.txt
COPY ./scraper .
CMD ["python3", "schedule_scraper.py"]