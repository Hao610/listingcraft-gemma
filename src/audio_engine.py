"""
ElevenLabs Audio Synthesis Client for E-Commerce Social Commerce.
Generates 30-second TikTok / Instagram Reels narration audio scripts for product listings.
"""

import os
import requests
from typing import Optional, Tuple


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - Clear, engaging marketing voice


def synthesize_marketing_audio(
    script_text: str,
    api_key: Optional[str] = None,
    voice_id: str = DEFAULT_VOICE_ID
) -> Tuple[Optional[bytes], str]:
    """
    Synthesizes engaging product marketing voiceover using ElevenLabs.
    Falls back gracefully to client-side Web Audio / TTS if API key is not supplied.
    """
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key or not key.strip():
        return None, "ElevenLabs API key not supplied. Using offline browser speech synthesis."

    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key.strip()
    }
    payload = {
        "text": script_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.85
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        if response.status_code == 200:
            return response.content, "Audio generated successfully via ElevenLabs Voice Engine."
        else:
            return None, f"ElevenLabs API returned {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return None, f"ElevenLabs synthesis error: {str(e)}"
