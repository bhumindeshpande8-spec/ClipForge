# backend/main.py
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os, shutil, asyncio

from transcription import transcribe
from rules import apply_rules
from renderer import render_video
from chat import apply_chat_command

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"


# ---------- Helpers ----------
async def run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


# ---------- /process (UPLOAD VIDEO) ----------
@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video_path_posix = Path(file_path).as_posix()

    try:
        segments = await run_in_thread(transcribe, video_path_posix)
        edit_plan = await run_in_thread(apply_rules, segments)
        output_video = await run_in_thread(render_video, file_path, edit_plan)
    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract audio or process video"
        )

    return {
        "video": output_video,
        "edits": edit_plan
    }


# ---------- /chat (EDIT VIA TEXT COMMAND) ----------
class ChatRequest(BaseModel):
    video_name: str
    message: str


@app.post("/chat")
async def chat_edit(payload: ChatRequest):
    video_path = os.path.join(UPLOAD_DIR, payload.video_name)

    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    video_path_posix = Path(video_path).as_posix()

    try:
        segments = await run_in_thread(transcribe, video_path_posix)
        edit_plan = await run_in_thread(apply_rules, segments)
        edit_plan = await run_in_thread(
            apply_chat_command, edit_plan, payload.message
        )
        output_video = await run_in_thread(render_video, video_path, edit_plan)
    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat edit"
        )

    return {
        "video": output_video,
        "edits": edit_plan
    }