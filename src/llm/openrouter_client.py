import os
import json
import requests
import time
from .prompts import build_script_prompt, build_manim_prompt
from .base_client import BaseLLMClient



class OpenRouterClient(BaseLLMClient):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "arcee-ai/trinity-large-preview:free"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_api_call(self, prompt: str):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 4000
        }

        for attempt in range(2):
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=300
            )

            if response.status_code != 200:
                print("STATUS:", response.status_code)
                print("BODY:", response.text)
                if attempt == 1:
                    raise Exception("LLM failed after 2 attempts.")
                time.sleep(2)
                continue

            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            # CLEAN MARKDOWN PROPERLY
            if content.startswith("```"):
                lines = content.splitlines()
                lines = lines[1:]  # remove ``` or ```python
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            return content

        raise Exception("LLM call failed.")

    # FIRST CALL: SCRIPT
    def generate_full_script(self, topic, num_sections):
        prompt = build_script_prompt(topic, num_sections)
        raw = self._make_api_call(prompt)
        return json.loads(raw)


    # SECOND CALL: MANIM CODE WITH DURATION
    def generate_manim_for_section(self, section, duration):
        prompt = build_manim_prompt(section, duration)
        return self._make_api_call(prompt)

