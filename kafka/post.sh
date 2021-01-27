#! /bin/sh

curl -H 'Content-Type: application/json' -X PUT -d @../kafka/DatabaseConnector.json localhost:8083/connectors/artists_connector/config;