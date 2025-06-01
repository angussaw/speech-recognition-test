#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

if [ -z "$INDEX_NAME" ]; then
    echo "Warning: INDEX_NAME not set in .env file, using default value 'cv-transcriptions'"
    INDEX_NAME="cv-transcriptions"
fi

if [ -z "$ELASTIC_PASSWORD" ]; then
    echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
    exit 1;
fi

curl -k -X PUT "https://localhost:9200/$INDEX_NAME" \
     -u "elastic:$ELASTIC_PASSWORD" \
     -H "Content-Type: application/json" \
     -d '{
       "settings": {
         "number_of_shards": 2,
         "number_of_replicas": 1
       },
        "mappings": {
            "properties": {
            "filename": {"type": "keyword"},
            "text": {"type": "text"},
            "up_votes": {"type": "integer"},
            "down_votes": {"type": "integer"},
            "age": {"type": "keyword","null_value": "unknown"},
            "gender": {"type": "keyword","null_value": "unknown"},
            "accent": {"type": "keyword","null_value": "unknown"},
            "duration": {"type": "float"},
            "generated_text": {"type": "text", "analyzer": "standard"}
            }
        }
     }'
