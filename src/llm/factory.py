# llm/factory.py

import os
from .openrouter_client import OpenRouterClient
from .gemini_client import GeminiClient
from .groq_client import GroqClient

def get_llm_client():

    provider = os.getenv("LLM_PROVIDER", "OPENROUTER").upper()

    if provider == "OPENROUTER":
        return OpenRouterClient()

    if provider == "GEMINI":
            return GeminiClient()
        
    if provider == "GROQ":
        return GroqClient()    

    raise Exception(f"Unknown LLM_PROVIDER: {provider}")



"""
Now you control provider via .env.

Example:

LLM_PROVIDER=openrouter
or
LLM_PROVIDER=openai

"""