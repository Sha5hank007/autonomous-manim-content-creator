# llm/groq_client.py

import os
import json
from groq import Groq
from .base_client import BaseLLMClient
from .prompts import build_script_prompt, build_manim_prompt


class GroqClient(BaseLLMClient):

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")

        # Force explicit key usage
        self.client = Groq(api_key=api_key)

        # Choose model here
        self.model = "openai/gpt-oss-120b"

    def _generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You generate structured JSON and valid Python code only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                stream=False
            )

            content = response.choices[0].message.content.strip()

            # Clean markdown fences
            if content.startswith("```"):
                lines = content.splitlines()
                lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            return content

        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    # FIRST CALL
    def generate_full_script(self, topic, num_sections):
        prompt = build_script_prompt(topic, num_sections)
        raw = self._generate(prompt)
        return json.loads(raw)

    # SECOND CALL
    def generate_manim_for_section(self, section, duration):
        prompt = build_manim_prompt(section, duration)
        return self._generate(prompt)
