# backend/renderer.py
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


def render_video(video_path, edit_plan):
    clip = VideoFileClip(video_path)
    txt_clips = []

    for e in edit_plan:
        txt = (
            TextClip(
                text=e["text"],
                font_size=24,
                font="Arial",
                method="caption",
                size=clip.size
            )
            .with_start(e["start"])
            .with_end(e["end"])
            .with_position(("center", "bottom"))
        )

        txt_clips.append(txt)

    final_video = (
        CompositeVideoClip([clip, *txt_clips])
        .with_audio(clip.audio)
    )

    output_path = os.path.join("outputs", os.path.basename(video_path))
    final_video.write_videofile(
        output_path,
        fps=clip.fps,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path