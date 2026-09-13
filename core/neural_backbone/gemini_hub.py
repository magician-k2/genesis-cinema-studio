import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

class GeminiHub:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyBkhM10sDbZGHmeBfeMGC6cgeIVr9qPvUk")
        self._client = None

    def get_client(self):
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[GeminiHub] Failed to init genai.Client: {e}", file=sys.stderr)
                return None
        return self._client

    def generate_text(self, prompt: str, model_name: str = "gemini-2.5-flash", system_instruction: str = None) -> str:
        client = self.get_client()
        if not client:
            return "Error: Gemini Client unavailable."
        try:
            from google.genai import types
            config = None
            if system_instruction:
                config = types.GenerateContentConfig(system_instruction=system_instruction)
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            return resp.text or ""
        except Exception as e:
            print(f"[GeminiHub] generate_text failed on {model_name}: {e}", file=sys.stderr)
            if "pro" in model_name:
                return self.generate_text(prompt, model_name="gemini-2.5-flash", system_instruction=system_instruction)
            return f"Error generating text: {e}"

gemini_hub = GeminiHub()
