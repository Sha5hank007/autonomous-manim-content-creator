import os
import subprocess
import tempfile
import shutil
from datetime import datetime


class ManimClient:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def render_animation(self, manim_code: str, section_index: int, section_title: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() else "_" for c in section_title)[:50]
        section_name = f"section_{section_index:02d}_{safe_title}"

        temp_dir = tempfile.mkdtemp(prefix="manim_")
        code_file = os.path.join(temp_dir, f"{section_name}.py")

        try:
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(manim_code)

            scene_class = self._extract_scene_class(manim_code)

            if not scene_class:
                return {
                    "success": False,
                    "video_path": None,
                    "error": "Scene class not found",
                    "logs": ""
                }

            cmd = [
                "manim",
                "-qm",
                "--format=mp4",
                "--media_dir", temp_dir,
                code_file,
                scene_class
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            logs = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"

            if result.returncode != 0:
                return {
                    "success": False,
                    "video_path": None,
                    "error": f"Manim exited with code {result.returncode}",
                    "logs": logs
                }

            video_search_path = os.path.join(temp_dir, "videos", section_name)

            rendered_video = None
            for root, _, files in os.walk(video_search_path):
                for file in files:
                    if file.endswith(".mp4"):
                        rendered_video = os.path.join(root, file)
                        break

            if not rendered_video:
                return {
                    "success": False,
                    "video_path": None,
                    "error": "Rendered video not found",
                    "logs": logs
                }

            final_video_name = f"{timestamp}_{section_name}.mp4"
            final_video_path = os.path.join(self.output_dir, final_video_name)

            shutil.copy2(rendered_video, final_video_path)

            return {
                "success": True,
                "video_path": final_video_path,
                "error": None,
                "logs": logs
            }

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _extract_scene_class(self, code: str):
        for line in code.split("\n"):
            line = line.strip()
            if line.startswith("class ") and "(Scene)" in line:
                return line.split("class ")[1].split("(")[0].strip()
        return None