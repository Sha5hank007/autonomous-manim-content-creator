# llm/base_client.py

from abc import ABC, abstractmethod


class BaseLLMClient(ABC):

    @abstractmethod
    def generate_full_script(self, topic: str, num_sections: int):
        pass

    @abstractmethod
    def generate_manim_for_section(self, section: dict, duration: float):
        pass
