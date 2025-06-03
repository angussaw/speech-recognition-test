FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY asr/asr_api.py .
COPY asr/models.py .
COPY .env .

EXPOSE 8001

CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001"]
