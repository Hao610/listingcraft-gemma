"""
ListingCraft AI Cross-Border Multi-Language Localizer & Currency Engine.
Localizes product titles, descriptions, and tags for high-spending global markets:
- Germany (Etsy DE / eBay DE) - EUR (€)
- France (Etsy FR / eBay FR) - EUR (€)
- Japan (Mercari / Rakuten) - JPY (¥)
- United Kingdom (Etsy UK) - GBP (£)
"""

import json
from typing import Dict, Any, Optional
import google.generativeai as genai


# Approximate exchange rates relative to USD
FX_RATES = {
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 152.0
}


def localize_listing(
    english_title: str,
    english_bullets: list,
    usd_price: float,
    target_locale: str = "German (DE)",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translates and culturally adapts listing copy for overseas buyers,
    converting pricing into local currency.
    """
    curr = "EUR" if "German" in target_locale or "French" in target_locale else ("JPY" if "Japan" in target_locale else "GBP")
    local_price = round(usd_price * FX_RATES[curr], 2 if curr != "JPY" else 0)

    # If no key, deliver deterministic localized template
    if not api_key or not api_key.strip():
        if "German" in target_locale:
            return {
                "locale": target_locale,
                "currency": curr,
                "local_price": local_price,
                "translated_title": f"[DE] Handgefertigte Vintage-Qualität | {english_title[:60]}",
                "translated_bullets": [
                    "Erstklassige Handwerkskunst mit langlebigen, hochwertigen Materialien.",
                    "Funktionales Design, ideal für den täglichen Gebrauch und besondere Anlässe.",
                    "Sorgfältig geprüft und authentisch im zeitlosen Vintage-Look."
                ],
                "local_tags": ["handgefertigt", "vintage stil", "geschenkidee", "nachhaltig"]
            }
        elif "French" in target_locale:
            return {
                "locale": target_locale,
                "currency": curr,
                "local_price": local_price,
                "translated_title": f"[FR] Artisanat Vintage de Qualité | {english_title[:60]}",
                "translated_bullets": [
                    "Conception artisanale d'exception avec des matériaux durables.",
                    "Style intemporel parfait pour le quotidien et les cadeaux raffinés.",
                    "Pièce authentique soigneusement inspectée."
                ],
                "local_tags": ["fait main", "vintage authentique", "cadeau artisanal", "deco"]
            }
        else: # Japanese
            return {
                "locale": target_locale,
                "currency": curr,
                "local_price": local_price,
                "translated_title": f"【美品】ヴィンテージ 手作り工芸品 | {english_title[:50]}",
                "translated_bullets": [
                    "厳選された上質な素材を使用した丁寧な職人技。",
                    "日常使いにも特別なギフトにも最適な機能的デザイン。",
                    "経年変化を楽しめる本物の風合い。"
                ],
                "local_tags": ["ハンドメイド", "ヴィンテージ", "工芸品", "ギフト"]
            }

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
Translate and culturally adapt this e-commerce listing for high-converting sales in {target_locale}.
Title: {english_title}
Bullet points: {json.dumps(english_bullets)}

Return STRICT JSON:
{{
  "translated_title": "<Localized title in {target_locale}>",
  "translated_bullets": ["<bullet 1 in {target_locale}>", "<bullet 2>", "<bullet 3>"],
  "local_tags": ["<tag 1>", "<tag 2>", "<tag 3>", "<tag 4>"]
}}
"""
        resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        parsed = json.loads(resp.text)
        parsed["locale"] = target_locale
        parsed["currency"] = curr
        parsed["local_price"] = local_price
        return parsed
    except Exception as e:
        return {
            "locale": target_locale,
            "currency": curr,
            "local_price": local_price,
            "translated_title": f"[{target_locale[:2].upper()}] {english_title}",
            "translated_bullets": english_bullets[:3],
            "local_tags": ["global shipping", "international", "artisanal"]
        }
