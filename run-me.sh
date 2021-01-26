#! /bin/sh

docker build -t spotifiy-api-scraper-image example-api-scrapper/.
cd docker
./restart.sh
cd ..
docker rm api-scraper
docker run -d --name api-scraper --env-file secrets.env --entrypoint tail spotifiy-api-scraper-image bash -f /dev/null
docker exec -it api-scraper bash