# Sreality scraping

## Project Overview

This project consists of three main components, each running in a separate docker container: a scraper, a server and PostgreSQL database. The Scraper is responsible for scraping estates from Sreality and saving them to the database. The server retrieves scraped estates from the database and serves them over HTTP in the form of HTML.

The code for each component resides in its own directory. The shared code for database access is encapsulated within the `estate_db` package, which is installed in each container during the build process.

## How to run locally?

To run the project locally, use the following command:

```
docker-compose up
```

Once launched, you can access the web UI at http://127.0.0.1:8080/.
