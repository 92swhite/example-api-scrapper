#! /bin/sh

curl -H 'Content-Type: application/json' -X DELETE localhost:8083/connectors/artists_connector | jq;
