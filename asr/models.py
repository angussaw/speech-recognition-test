from pydantic import BaseModel, Field


class TranscriptionResponse(BaseModel):
    transcription: str = Field(
        ..., description="The transcribed text returned by the model"
    )
    duration: str = Field(..., description="Duration of the audio file in seconds")
