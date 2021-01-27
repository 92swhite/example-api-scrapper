#! /bin/sh

cd docker/
docker-compose down -v
docker stop api-scraper
docker rm api-scraper