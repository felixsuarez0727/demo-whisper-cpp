from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import shutil
import os
import time
from whispercpp import Whisper
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Initialize Whisper model
    w = Whisper("small")  # Options: "tiny", "small", "base", "medium", "large"
    # Create a temporary directory to store the uploaded audio file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    audio_path = os.path.join(temp_dir, file.filename)

    # Save the uploaded audio file
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:

        start_time = time.time()

        # Perform transcription
        result = w.transcribe(audio_path)

        end_time = time.time()

        # Calculate processing time
        processing_time_seconds = end_time - start_time

        # Check if transcription was successful
        if result == 0:
            # Extract transcribed text
            text = w.extract_text(result)
            transcription = "\n".join(text)
        else:
            # Transcription failed
            transcription = f"Transcription failed with error code: {result}"

        # Construct processing time string
        hours = int(processing_time_seconds // 3600)
        minutes = int((processing_time_seconds % 3600) // 60)
        seconds = int(processing_time_seconds % 60)
        processing_time = "%d hours, %d minutes, %d seconds" % (
            hours, minutes, seconds)

        # Remove the uploaded audio file
        shutil.rmtree(temp_dir)

        # Return transcription result
        transcription_result = f"{transcription}\n\nProcessing time: {processing_time}"
        return PlainTextResponse(transcription_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
