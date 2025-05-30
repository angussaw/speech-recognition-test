import io
from typing import List

import librosa
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import TranscriptionResponse
from transformers import pipeline

app = FastAPI(title="asr", version="fastapi:1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transcription_pipeline = pipeline(
    "automatic-speech-recognition", model="facebook/wav2vec2-large-960h"
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
    results = []

    for file in files:
        try:
            content = await file.read()

            audio_data, sampling_rate = librosa.load(io.BytesIO(content), sr=None)
            if sampling_rate != 16000:
                audio_data = librosa.resample(
                    y=audio_data, orig_sr=sampling_rate, target_sr=16000
                )

            result = transcription_pipeline(inputs=audio_data, return_timestamps="word")

            transcription = result["text"]
            chunks = result["chunks"]
            duration = chunks[-1]["timestamp"][1]

            results.append(
                TranscriptionResponse(
                    transcription=transcription, duration=str(duration)
                )
            )
            await file.close()

        except Exception as e:
            print(f"Error processing file {file.filename}: {str(e)}")
            continue

    return results
