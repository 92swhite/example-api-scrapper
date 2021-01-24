#! /bin/sh

set -o allexport
. ../secrets.env
docker-compose down -v
docker-compose up -d
set +o allexport