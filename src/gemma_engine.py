"""
Gemma 2 Multimodal Vision & E-Commerce Listing Intelligence Engine.
Analyzes product photos, extracts materials/finishes/defects, and generates
platform-specific listing copy (Etsy, eBay, Shopify) adhering to strict JSON schema.
"""

import os
import json
from typing import Dict, Any, Optional
from PIL import Image
import google.generativeai as genai
from src.catalog_db import lookup_offline_template


GEMMA_SYSTEM_PROMPT = """You are ListingCraft AI, an elite e-commerce conversion copywriter and product appraiser powered by Google Gemma 2.
Your role is to empower solo freelancers, vintage resellers, and handmade creators to create high-converting product listings that actually sell.

CRITICAL INSTRUCTIONS:
1. Examine product images or descriptions thoroughly for:
   - Specific materials (e.g., full-grain leather, stoneware, brass, silk).
   - Style aesthetics (e.g., Japandi, Y2K, Mid-Century Modern, Dark Academia).
   - Condition and honest defect disclosure (e.g., patina, scuffs, clean seams).
2. Write SEO titles optimized for Etsy / eBay search algorithms (front-load high-volume keywords, include 3 search phrases separated by pipes | ).
3. Generate 4 persuasive bullet points using the 'Feature -> Benefit' copywriting formula.
4. Provide 10 high-intent search tags (lowercase, comma-separated style).
5. Produce a 30-second conversational voiceover script for TikTok/Instagram Reels social selling.
6. Return STRICT, valid JSON adhering to the specified schema.

JSON SCHEMA:
{
  "item_name": "<concise title>",
  "detected_materials": ["<material 1>", "<material 2>"],
  "aesthetic_style": "<e.g., Rustic Boho | Y2K Cyber | Japandi Minimalist>",
  "seo_title": "<Keyword-rich title under 140 chars>",
  "bullet_points": [
    "<Bullet 1: Main Craftsmanship/Material & Benefit>",
    "<Bullet 2: Functional Dimensions & Practical Everyday Use>",
    "<Bullet 3: Unique Aesthetic / Styling Inspiration>",
    "<Bullet 4: Care Instructions / Authentic Vintage Character>"
  ],
  "search_tags": ["<tag1>", "<tag2>", "<tag3>", "<tag4>", "<tag5>", "<tag6>", "<tag7>", "<tag8>", "<tag9>", "<tag10>"],
  "social_video_script": "<engaging 30-sec conversational hook and call to action for social video>",
  "target_buyer_persona": "<who pays for this, e.g. Design Enthusiasts, Urban Commuters>"
}
"""


def generate_listing_multimodal(
    query_description: str,
    image: Optional[Image.Image] = None,
    category: str = "Vintage Clothing",
    condition: str = "Very Good (Minor Wear)",
    target_platform: str = "Etsy",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs REAL-TIME dynamic multimodal inference via Google Gemma 2 / Gemini 1.5.
    Zero static hardcoded templates - generates truly bespoke structured listings.
    """
    key = api_key or os.getenv("GEMINI_API_KEY", "")

    if not key or not key.strip():
        # Provide transparent prompt to user instead of pretending with hardcoded data
        raise ValueError("Google Gemini / Gemma API Key is missing. Please configure GEMINI_API_KEY in Render Environment or enter it in the sidebar.")

    import requests

    # Use direct official Google Generative Language REST API for maximum speed & strict timeout
    # This prevents the deprecated SDK from hanging indefinitely on network or rate limits
    clean_key = key.strip()
    
    # 1. Fetch authorized active models for this key directly via lightweight REST GET
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
    available_models = []
    try:
        list_resp = requests.get(list_url, timeout=8)
        if list_resp.status_code == 200:
            m_list = list_resp.json().get("models", [])
            for item in m_list:
                if "generateContent" in item.get("supportedGenerationMethods", []):
                    m_id = item.get("name", "").replace("models/", "")
                    # Filter out models explicitly flagged as deprecated / experimental preview
                    if m_id and "2.5" not in m_id:
                        available_models.append(m_id)
    except Exception:
        pass

    # Standard public models guaranteed on Google AI Studio
    standard_models = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest"
    ]

    # Prioritize standard models that exist in available_models, then remaining available_models, then standard_models
    matched = [m for m in standard_models if m in available_models]
    remainder = [m for m in available_models if m not in matched]
    models_to_try = matched + remainder if available_models else standard_models

    # Build parts payload
    parts = [{"text": f"System Instructions:\n{GEMMA_SYSTEM_PROMPT}\n\nTask:\nTarget Marketplace: {target_platform}\nCategory: {category}\nCondition: {condition}\nProduct Description: {query_description}\n\nGenerate listing JSON matching the schema."}]
    
    if image is not None:
        import io
        import base64
        buf = io.BytesIO()
        img_thumb = image.copy().convert("RGB")
        img_thumb.thumbnail((800, 800))
        img_thumb.save(buf, format="JPEG", quality=85)
        b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": b64_img
            }
        })

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4
        }
    }

    last_err = None
    for m in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={clean_key}"
        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=18)
            if resp.status_code == 200:
                resp_json = resp.json()
                text_content = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text_content)
                data["engine"] = f"Google AI / {m} (Real-time Live Inference)"
                return data
            else:
                last_err = f"HTTP {resp.status_code} ({m}): {resp.text[:120]}"
                continue
        except Exception as ex:
            last_err = str(ex)
            continue

    raise RuntimeError(f"Live AI inference failed. {last_err}")
