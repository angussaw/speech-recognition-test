# Speech Recognition Test

## A. Developer Setup

### Installation

1. Create and activate a virtual environment:

   ```
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. Install dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

3. Install pre-commit hooks:

   ```
   pre-commit install
   ```

4. Install ffmpeg

## B. Running Automatic Speech Recognition Microservice Locally

1. Build and run the image

```
docker build -t asr-api -f asr/Dockerfile .

docker run --rm -p 8001:8001 --name asr-api asr-api
```

2. Test the endpoint using CURL

```
curl -F ‘files=@/path/to/audio-file/sample-000000.mp3’ http://localhost:8001/asr
```

3. Place all audio files in a folder named `cv-valid-dev`

4. Create an `.env` file and update a suitable `BATCH_SIZE` value. (defaults to 20)

```
cp .env.example .env
```

5. Run `asr/cv-decode.py` at the root level, specifying the path of the audio files (`cv-valid-dev`) and the csv files to save the generated texts to

```
python asr/cv-decode.py cv-valid-dev <save_csv_file_name>
```
