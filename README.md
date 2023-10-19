# Sreality scraping

## Project Overview

This project consists of three main components, each running in a separate docker container: a scraper, a server and a PostgreSQL database. The scraper is responsible for scraping estates from [Sreality](https://www.sreality.cz/) and saving them to the database. The scraping process occurs upon container launch and repeats every 5 minutes, gathering the initial 500 results (ignoring entries already present in the database). The server retrieves scraped estates from the database and serves them over HTTP in the form of HTML.

The code for each component resides in its own directory. The shared code for database access is encapsulated within the `estate_db` package, which is installed in each container during the build process.

## How to run locally?

To run the project locally, use the following command:

```
docker-compose up
```

Once launched, you can access the web UI at http://127.0.0.1:8080/.
