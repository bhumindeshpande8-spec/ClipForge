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


# --- Pydantic model matching frontend JSON ---
class ChatRequest(BaseModel):
    video_name: str
    message: str

# --- Async wrapper for blocking functions ---
async def run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

@app.post("/chat")
async def chat_edit(payload: ChatRequest):
    video_name = payload.video_name
    message = payload.message

    # Build path to uploaded video
    video_path = os.path.join("uploads", video_name)
    video_path_posix = Path(video_path).as_posix()

    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    try:
        # Transcribe video
        segments = await run_in_thread(transcribe, video_path_posix)

        # Generate edit plan and apply chat command
        edit_plan = await run_in_thread(apply_rules, segments)
        edit_plan = await run_in_thread(apply_chat_command, edit_plan, message)

        # Render final video
        output_video = await run_in_thread(render_video, video_path, edit_plan)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Failed to extract audio or process video.")

    return {
        "video": output_video,
        "edits": edit_plan
    }