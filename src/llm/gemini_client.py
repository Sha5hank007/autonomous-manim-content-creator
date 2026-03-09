# llm/gemini_client.py

import os
import json
from google import genai
from .base_client import BaseLLMClient
from .prompts import build_script_prompt, build_manim_prompt


class GeminiClient(BaseLLMClient):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")

        # Forcing use of this key explicitly
        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-2.5-flash"

    def _generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            if not response.text:
                raise Exception("Gemini returned empty response.")

            content = response.text.strip()

            # Clean markdown fences if present
            if content.startswith("```"):
                lines = content.splitlines()
                lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            return content

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    # FIRST CALL
    def generate_full_script(self, topic, num_sections):
        prompt = build_script_prompt(topic, num_sections)
        raw = self._generate(prompt)
        return json.loads(raw)

    # SECOND CALL
    def generate_manim_for_section(self, section, duration):
        prompt = build_manim_prompt(section, duration)
        return self._generate(prompt)
