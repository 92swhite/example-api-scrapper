#! /bin/sh

curl -H 'Content-Type: application/json' -X PUT -d @DatabaseConnector.json localhost:8083/connectors/artists_connector/config | jq;