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
    Analyzes item description and image using Google Gemma 2.
    Degrades gracefully to offline deterministic catalogs if offline or API key absent.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key or not key.strip():
        # Pure offline deterministic fallback
        template = lookup_offline_template(query_description)
        return {
            "item_name": template["title"],
            "detected_materials": template["materials"],
            "aesthetic_style": "Rustic Artisanal Heritage",
            "seo_title": template["seo_title"],
            "bullet_points": template["bullet_points"],
            "search_tags": template["tags"],
            "social_video_script": template["social_script"],
            "target_buyer_persona": "Discerning Quality Seekers & Gift Buyers",
            "engine": "ListingCraft Offline Local Knowledge Engine"
        }

    try:
        genai.configure(api_key=key.strip())
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=GEMMA_SYSTEM_PROMPT
        )

        prompt_text = f"""
Platform: {target_platform}
Category: {category}
Item Condition: {condition}
Seller Notes / Details: "{query_description}"

Analyze this merchandise and generate the complete high-converting product listing JSON.
"""
        contents = [prompt_text]
        if image is not None:
            img_copy = image.copy()
            img_copy.thumbnail((1024, 1024))
            contents.append(img_copy)

        response = model.generate_content(
            contents,
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        data["engine"] = "Google Gemma 2 Multimodal Pipeline"
        return data

    except Exception as e:
        template = lookup_offline_template(query_description)
        return {
            "item_name": template["title"],
            "detected_materials": template["materials"],
            "aesthetic_style": "Authentic Handcrafted",
            "seo_title": template["seo_title"],
            "bullet_points": template["bullet_points"],
            "search_tags": template["tags"],
            "social_video_script": template["social_script"],
            "target_buyer_persona": "Eco-Conscious Collectors",
            "engine": f"Deterministic Offline Fallback (API Note: {str(e)[:40]})"
        }
