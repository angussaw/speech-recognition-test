# Speech Recognition Test

## A. Developer Setup and Installation

#### 1. Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

#### 2. Install dependencies using pip:

```
pip install -r requirements.txt
```

#### 3. Install pre-commit hooks:

```
pre-commit install
```

#### 4. Install ffmpeg

## B. Running Automatic Speech Recognition microservice locally

#### 1. Build and run the image

```
docker build -t asr-api -f asr/Dockerfile .

docker run --rm -p 8001:8001 --name asr-api asr-api
```

#### 2. Test the endpoint using CURL

```
curl -F ‘files=@/path/to/audio-file/MKH800_19_0001.wav’ http://localhost:8001/asr
```

```json
[
  {
    "transcription": "SHE HAD YOUR DARK SUIT IN GREASY WASH WATER ALL YEAR",
    "duration": "3.62"
  }
]
```

#### 3. Place all audio files in a folder named `cv-valid-dev`

#### 4. Create an `.env` file and update a suitable `BATCH_SIZE` value. (defaults to 20)

```
cp .env.example .env
```

```
BATCH_SIZE=
```

#### 5. Run `asr/cv-decode.py` at the root level, specifying the path of the audio files (`cv-valid-dev`) and the csv file to save the generated texts to

```
python asr/cv-decode.py cv-valid-dev <save_csv_file_name>
```

## C. Setting up the elastic search backend locally

#### 1. In the .env file, update the following variables

```
ELASTIC_PASSWORD=
CLUSTER_NAME=asr-es-cluster
INDEX_NAME=cv-transcriptions
ES_PORT=9200
```

#### 2. Start the services

```
docker compose -f elastic-backend/docker-compose.yml --env-file .env up
```

#### 3. After the services are up, create an index called `cv-transcriptions` by running the `elastic-backend/create-index.sh` script

```
bash elastic-backend/create-index.sh
```

#### 4. Verify that the index has been created succcesfully:

```
curl -k -X GET "https://localhost:9200/_cat/indices" -u "elastic:$ELASTIC_PASSWORD"
```

```
green open cv-transcriptions _VMzGXqYRdCtbXqEo88taA 2 1 4076 0 1.8mb 973kb 973kb
```

```
curl -k -X GET "https://localhost:9200/cv-transcriptions/_count?pretty" -u "elastic:$ELASTIC_PASSWORD"
```

```json
{
  "count": 0,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  }
}
```

#### 5. After the index is created, run `elastic-backend/cv-index.py` at the root level, specifying the path of the csv file containing the generated texts

```
python elastic-backend/cv-index.py <records_path>
```

#### 6. Verify that the records have been succesfully indexed

```
curl -k -X GET "https://localhost:9200/cv-transcriptions/_search?size=2&pretty" -u "elastic:$ELASTIC_PASSWORD"
```

```json
{
  "took": 11,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4076,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "cv-transcriptions",
        "_id": "tMuXKZcB4uKBUf0WHfFH",
        "_score": 1.0,
        "_source": {
          "filename": "cv-valid-dev/sample-000000.mp3",
          "text": "be careful with your prognostications said the stranger",
          "up_votes": 1,
          "down_votes": 0,
          "age": null,
          "gender": null,
          "accent": null,
          "duration": 4.36,
          "generated_text": "BE CAREFUL WITH YOUR PROGNOSTICATIONS SAID THE STRANGER"
        }
      },
      {
        "_index": "cv-transcriptions",
        "_id": "tcuXKZcB4uKBUf0WHfFI",
        "_score": 1.0,
        "_source": {
          "filename": "cv-valid-dev/sample-000001.mp3",
          "text": "then why should they be surprised when they see one",
          "up_votes": 2,
          "down_votes": 0,
          "age": null,
          "gender": null,
          "accent": null,
          "duration": 2.38,
          "generated_text": "THEN WHY SHOULD THEY BE SURPRISED WHEN THEY SEE ONE"
        }
      }
    ]
  }
}
```
