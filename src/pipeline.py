import json
import subprocess
from pathlib import Path
from datetime import datetime
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    ImageClip,
)

from llm.factory import get_llm_client
from manim_client import ManimClient
from tts_client import synthesize_to_temp_mp3


class VideoPipeline:
    def __init__(self):
        self.llm = get_llm_client()
        self.manim = None

    def run(self, topic: str, num_sections: int = 3,
            voice: str = "en-US-JennyNeural",
            rate: str = "+0%"):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_")

        run_dir = Path("runs") / f"{safe_topic}_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)

        self.manim = ManimClient(str(run_dir))

        log_file = run_dir / "llm_log.md"

        def log(title, content):
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n# {title}\n\n")
                f.write("```\n")
                f.write(str(content))
                f.write("\n```\n")

        try:
            full_script = self.llm.generate_full_script(topic, num_sections)
            log("SCRIPT_JSON", json.dumps(full_script, indent=2))
        except Exception as e:
            return {"success": False, "error": str(e)}

        section_videos = []
        raw_renders = []
        failed_sections = []

        for i, section in enumerate(full_script["sections"]):
            idx = i + 1

            try:
                audio_path = synthesize_to_temp_mp3(
                    text=section["narration"],
                    run_audio_dir=str(run_dir),
                    filename=f"section_{idx}.mp3",
                    voice=voice,
                    rate=rate
                )
                 
                audio_clip = None
                video_clip = None
                final_clip = None 
                
                audio_clip = AudioFileClip(audio_path)
                audio_duration = audio_clip.duration

                log(f"AUDIO_DURATION_SECTION_{idx}", audio_duration)

                manim_code = self.llm.generate_manim_for_section(section, audio_duration)
                log(f"MANIM_CODE_SECTION_{idx}", manim_code)

                code_path = run_dir / f"section_{idx}.py"
                code_path.write_text(manim_code)

                render_result = self.manim.render_animation(
                    manim_code=manim_code,
                    section_index=idx,
                    section_title=section["title"]
                )

                if not render_result["success"]:
                    print(f"❌ Section {idx} render failed")

                    log(f"SECTION_{idx}_RENDER_FAILED", render_result["error"])

                    failed_code_path = run_dir / f"section_{idx}_FAILED.py"
                    code_path.rename(failed_code_path)

                    failed_sections.append(idx)
                    continue

                video_path = render_result["video_path"]
                raw_renders.append(video_path)

                video_clip = VideoFileClip(video_path)
                video_duration = video_clip.duration

                if audio_duration > video_duration:
                    last_frame = video_clip.get_frame(video_duration - 0.01)
                    freeze_duration = audio_duration - video_duration
                    freeze_clip = ImageClip(last_frame).with_duration(freeze_duration)
                    video_clip = concatenate_videoclips([video_clip, freeze_clip])

                final_clip = video_clip.with_audio(audio_clip)

                section_video_path = run_dir / f"section_{idx}_final.mp4"

                final_clip.write_videofile(
                    str(section_video_path),
                    codec="libx264",
                    audio_codec="aac"
                )


                section_videos.append(str(section_video_path))
                
            except Exception as e:
                print(f"❌ Section {idx} pipeline failed")
                log(f"SECTION_{idx}_PIPELINE_ERROR", str(e))
                failed_sections.append(idx)
                continue
                
            finally:
                    try:
                        if final_clip:
                            final_clip.close()
                    except:
                        pass

                    try:
                        if video_clip:
                            video_clip.close()
                    except:
                        pass

                    try:
                        if audio_clip:
                            audio_clip.close()
                    except:
                        pass    

            

        if not section_videos:
            return {"success": False, "error": "All sections failed"}

        final_path = run_dir / f"{safe_topic}_final.mp4"

        list_file = run_dir / "concat_list.txt"

        with open(list_file, "w", encoding="utf-8") as f:
            for path in section_videos:
                absolute_path = Path(path).resolve()
                f.write(f"file '{absolute_path.as_posix()}'\n")

        subprocess.run(
    [
        "ffmpeg",
        "-loglevel", "error",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(final_path)
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=True
)

        list_file.unlink(missing_ok=True)

        if failed_sections:
            log("FAILED_SECTIONS", failed_sections)

        # cleanup
        for path in section_videos:
            Path(path).unlink(missing_ok=True)

        for path in raw_renders:
            Path(path).unlink(missing_ok=True)

        for mp3 in run_dir.glob("section_*.mp3"):
            mp3.unlink(missing_ok=True)

        return {"success": True, "final_video": str(final_path)}