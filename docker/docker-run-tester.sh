#! /bin/sh

cd ..
docker stop api-example-tester
docker rm api-example-tester
docker build -t api-example example-api-scrapper/
docker run -d --network host --name api-example-tester -v $(pwd):/dockertesting/ --entrypoint tail api-example:latest -f /dev/null
docker exec -it api-example-tester bash