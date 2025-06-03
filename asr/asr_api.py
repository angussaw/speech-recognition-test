import io
import logging
import os
from typing import List

import librosa
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import TranscriptionResponse
from transformers import pipeline

load_dotenv()

app = FastAPI(title="asr", version="fastapi:1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("asr-microservice")

transcription_pipeline = pipeline(
    "automatic-speech-recognition", model=os.getenv("HF_MODEL_NAME")
)


@app.get("/ping")
async def health_check():
    return "pong"


@app.post("/asr", response_model=List[TranscriptionResponse])
async def transcribe_audio(files: List[UploadFile] = File(...)):
    """
    Process multiple audio files and return their transcriptions.

    Args:
        files (List[UploadFile]): List of audio files uploaded via multipart/form-data.
            Supports MP3 and other common audio formats.

    Returns:
        List[TranscriptionResponse]: List of transcription results, each containing:
            - transcription (str): The transcribed text
            - duration_seconds (str): Duration of the audio in seconds

    """
    inputs = []
    results = []

    for file in files:
        content = await file.read()

        audio_data, sampling_rate = librosa.load(io.BytesIO(content), sr=None)
        if sampling_rate != 16000:
            audio_data = librosa.resample(
                y=audio_data, orig_sr=sampling_rate, target_sr=16000
            )

        inputs.append(audio_data)
        await file.close()

    try:
        outputs = transcription_pipeline(inputs=inputs, return_timestamps="word")

        for output in outputs:
            transcription = output["text"]
            chunks = output["chunks"]
            duration = 0
            if (
                chunks
                and "timestamp" in chunks[-1]
                and len(chunks[-1]["timestamp"]) > 1
            ):
                duration = chunks[-1]["timestamp"][1]

            results.append(
                TranscriptionResponse(
                    transcription=transcription, duration=str(duration)
                )
            )

        logger.info(f"Successfully transcribed {len(files)} audio files")

        return results

    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return [TranscriptionResponse(transcription="", duration="") for _ in files]
