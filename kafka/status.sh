#! /bin/sh

curl -H 'Content-Type: application/json' localhost:8083/connectors/artists_connector/status | jq;
