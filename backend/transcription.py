# backend/transcription.py
import whisper

model = whisper.load_model("base")  # Allowed component model

def transcribe(video_path: str):
    """
    Convert speech → text + timestamps
    """
    result = model.transcribe(video_path)
    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })
    return segments