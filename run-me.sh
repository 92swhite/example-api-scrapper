#! /bin/sh

cd docker
./restart.sh
cd ..
docker build -t spotifiy-api-scraper-image .
docker stop api-scraper
docker rm api-scraper
docker run -d --name api-scraper --network host --env-file secrets.env --entrypoint tail spotifiy-api-scraper-image bash -f /dev/null
docker exec -it api-scraper bash