# backend/main.py
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
import os, shutil

from backend.transcription import transcribe
from backend.rules import apply_rules
from backend.renderer import render_video
from backend.chat import apply_chat_command


app = FastAPI()
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert path to POSIX style for Whisper/FFmpeg
    video_path = Path(file_path).as_posix()

    # Transcribe with error handling
    try:
        segments = transcribe(video_path)
    except RuntimeError as e:
        return {"error": "Failed to extract audio. Check video format or FFmpeg installation."}

    # Apply editing rules and render video
    edit_plan = apply_rules(segments)
    output_video = render_video(file_path, edit_plan)

    return {"video": output_video, "edits": edit_plan}


@app.post("/chat")
async def chat_edit(video_name: str, message: str):
    # Ensure path is correct
    video_path = os.path.join(UPLOAD_DIR, video_name)
    video_path_posix = Path(video_path).as_posix()

    # Transcribe with error handling
    try:
        segments = transcribe(video_path_posix)
    except RuntimeError as e:
        return {"error": "Failed to extract audio. Check video format or FFmpeg installation."}

    # Apply rules and chat commands
    edit_plan = apply_rules(segments)
    edit_plan = apply_chat_command(edit_plan, message)
    output_video = render_video(video_path, edit_plan)

    return {"video": output_video, "edits": edit_plan}
