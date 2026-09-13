import os
import json
from pathlib import Path
from .gemini_hub import gemini_hub
from .vault_service import vault_service

class MusicRouter:
    @staticmethod
    def handle_produce_prompt(payload: dict) -> dict:
        topic = payload.get("topic", "Cyberpunk Night Drive")
        genre = payload.get("genre", "Synthwave")
        mood = payload.get("mood", "Energetic, Melancholic")
        bpm = payload.get("bpm", 128)
        instruments = payload.get("instruments", "Analog synths, 808 drum machine, distorted bass")
        lyrics = payload.get("lyrics", "")

        prompt = f"""You are a world-class Music Producer and Prompt Engineer for state-of-the-art AI Music Generators (MiniMax Music-01, Udio, Suno).
Based on the following request, generate a highly detailed, professional, structured music prompt and lyrical arrangement.

Topic/Theme: {topic}
Genre/Style: {genre}
Mood: {mood}
BPM: {bpm}
Key Instruments: {instruments}
User Provided Lyrics/Notes: {lyrics}

Respond with strict JSON adhering to this format:
{{
  "title": "Track Title",
  "style_tags": "Genre, Sub-genre, Mood, Instrument tags separated by commas",
  "bpm": 128,
  "key_signature": "e.g. F# Minor",
  "minimax_prompt": "Dense, highly evocative paragraph describing the sound texture, mix, era, mastering, and dynamic curve for MiniMax Music-01 prompt input",
  "lyrics_structure": "[Verse 1]\n...\n\n[Chorus]\n...\n\n[Drop/Solo]\n...",
  "production_notes": "Advice on stems, vocal chain, and mixing aesthetics"
}}"""
        raw_text = gemini_hub.generate_text(prompt, model_name="gemini-2.5-flash")
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "title": f"{topic} ({genre})",
                "style_tags": f"{genre}, {mood}",
                "bpm": bpm,
                "key_signature": "A Minor",
                "minimax_prompt": raw_text,
                "lyrics_structure": lyrics or "[Verse 1]\nNeon lights in the rain\nEchoes calling your name",
                "production_notes": "Generated with Gemini fallback parsing"
            }

    @staticmethod
    def handle_reverse_engineer(payload: dict) -> dict:
        filename = payload.get("filename", "audio_sample.mp3")
        file_meta = payload.get("meta", {})
        prompt = f"""You are a master Audio Mastering Engineer and Reverse-Engineering Expert.
Analyze the following audio track metadata/description and reverse-engineer its exact musical DNA and AI prompt reconstruction:

Audio: {filename}
Metadata: {json.dumps(file_meta, ensure_ascii=False)}

Output strict JSON:
{{
  "detected_genre": "Specific Genre & Era",
  "detected_bpm": 124,
  "estimated_key": "C Minor",
  "timbre_analysis": "Detailed description of drum punch, bass harmonics, vocal treatment, stereophony",
  "reconstructed_minimax_prompt": "The exact prompt you would feed into MiniMax or Suno to reproduce this sonic signature",
  "stem_recommendations": {{
    "drums": "Kick/Snare character",
    "bass": "Bassline synthesis method",
    "vocals": "Reverb/delay chain",
    "synths": "Lead and pad characteristics"
  }}
}}"""
        raw_text = gemini_hub.generate_text(prompt, model_name="gemini-2.5-flash")
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "detected_genre": "Electronic",
                "detected_bpm": 120,
                "reconstructed_minimax_prompt": raw_text
            }
