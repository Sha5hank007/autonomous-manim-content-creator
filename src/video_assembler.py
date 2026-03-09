# video_assembler.py
from moviepy import VideoFileClip, concatenate_videoclips

def assemble_sections_to_video(video_paths: list[str], out_path: str):
    """
    Concatenates a list of section mp4s into a single mp4.
    Each section should already have its audio attached.
    """
    clips = [VideoFileClip(path) for path in video_paths]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(out_path, codec="libx264")
