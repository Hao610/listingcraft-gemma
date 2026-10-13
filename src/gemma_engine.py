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

    genai.configure(api_key=key.strip())
    
    # Dynamically query exactly which models this specific API key is authorized to call
    available_models = []
    try:
        for m in genai.list_models():
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                clean_name = m.name.replace("models/", "")
                available_models.append(clean_name)
    except Exception:
        pass

    priority_candidates = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]

    if available_models:
        candidate_models = [m for m in priority_candidates if m in available_models]
        if not candidate_models:
            candidate_models = available_models
    else:
        candidate_models = priority_candidates

    prompt_text = f"""
Target Marketplace: {target_platform}
Product Category: {category}
Item Condition: {condition}
Seller Description / Visual Notes: "{query_description}"

Generate a 100% bespoke, non-generic, high-converting e-commerce listing in structured JSON format matching the schema.
Extract real product characteristics from the provided input and image.
"""
    contents = [prompt_text]
    if image is not None:
        img_copy = image.copy().convert("RGB")
        img_copy.thumbnail((1024, 1024))
        contents.append(img_copy)

    last_err = None
    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=GEMMA_SYSTEM_PROMPT
            )
            response = model.generate_content(
                contents,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            data["engine"] = f"Google AI / {model_name} (Live Multimodal)"
            return data
        except Exception as err:
            last_err = err
            continue

    raise RuntimeError(f"Attempted models {candidate_models[:5]}. Error: {last_err}")
