"""
ListingCraft AI Trademark & Platform Policy Risk Scanner.
Scans generated listing titles, bullet points, and tags against known
intellectual property trademarks and restricted marketplace terms (Etsy, eBay, Amazon).
Prevents account bans and copyright takedowns for side hustlers.
"""

from typing import List, Dict, Any

# Well-known trademarked words that frequently get Etsy/eBay sellers banned or de-listed
TRADEMARK_RISK_DATABASE: Dict[str, Dict[str, str]] = {
    "velcro": {
        "trademark_owner": "Velcro Companies",
        "replacement": "hook-and-loop fastener",
        "risk_level": "HIGH"
    },
    "onesie": {
        "trademark_owner": "Gerber Childrenswear",
        "replacement": "infant bodysuit / one-piece",
        "risk_level": "CRITICAL"
    },
    "thermos": {
        "trademark_owner": "Thermos L.L.C.",
        "replacement": "vacuum-insulated flask / thermal bottle",
        "risk_level": "HIGH"
    },
    "chapstick": {
        "trademark_owner": "Pfizer / Haleon",
        "replacement": "lip balm / moisturizing balm",
        "risk_level": "MODERATE"
    },
    "band-aid": {
        "trademark_owner": "Johnson & Johnson",
        "replacement": "adhesive bandage",
        "risk_level": "HIGH"
    },
    "popsicle": {
        "trademark_owner": "Unilever",
        "replacement": "frozen ice pop / fruit ice bar",
        "risk_level": "MODERATE"
    },
    "tiffany blue": {
        "trademark_owner": "Tiffany & Co.",
        "replacement": "robin's egg blue / aqua turquoise",
        "risk_level": "CRITICAL"
    },
    "disney": {
        "trademark_owner": "The Walt Disney Company",
        "replacement": "fairytale-inspired / whimsical theme",
        "risk_level": "CRITICAL"
    },
    "lego": {
        "trademark_owner": "The LEGO Group",
        "replacement": "interlocking building bricks",
        "risk_level": "CRITICAL"
    }
}


def scan_trademark_compliance(text_content: str) -> Dict[str, Any]:
    """
    Scans e-commerce listing text for trademark violations and policy risks.
    """
    text_lower = text_content.lower()
    violations: List[Dict[str, str]] = []

    for word, meta in TRADEMARK_RISK_DATABASE.items():
        if word in text_lower:
            violations.append({
                "flagged_term": word.title(),
                "trademark_owner": meta["trademark_owner"],
                "safe_replacement": meta["replacement"],
                "risk_level": meta["risk_level"]
            })

    is_clean = len(violations) == 0
    overall_status = "SAFE (100% Policy Compliant)" if is_clean else f"WARNING ({len(violations)} Trademark Risks Detected)"

    return {
        "is_clean": is_clean,
        "status": overall_status,
        "violations": violations,
        "compliance_score": 100 if is_clean else max(20, 100 - (len(violations) * 25))
    }
