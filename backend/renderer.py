# backend/renderer.py
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def render_video(video_path, edit_plan):
    """
    Overlay captions on video
    """
    clip = VideoFileClip(video_path)
    txt_clips = []

    for e in edit_plan:
        txt = TextClip(e["text"], fontsize=24, color="white")
        txt = txt.set_start(e["start"]).set_end(e["end"]).set_position(("center", "bottom"))
        txt_clips.append(txt)

    video = CompositeVideoClip([clip, *txt_clips])
    output_path = os.path.join("outputs", os.path.basename(video_path))
    video.write_videofile(output_path, fps=clip.fps)
    return output_path
