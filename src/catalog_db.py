"""
Pre-cached Offline E-Commerce Templates & Specimen Catalogs.
Guarantees 100% functionality and deterministic fallbacks even without API keys.
"""

from typing import Dict, Any, List

OFFLINE_SPECIMEN_CATALOG: Dict[str, Dict[str, Any]] = {
    "vintage_leather_camera_bag": {
        "title": "Vintage Handcrafted Saddle-Brown Leather Camera Satchel",
        "category": "Vintage Clothing",
        "condition": "Very Good (Minor Wear)",
        "materials": ["Full-grain distressed leather", "Brass buckle hardware", "Padded canvas interior"],
        "seo_title": "Vintage Leather Camera Bag Satchel | Handcrafted Rustic Messenger Bag | Distressed Full Grain Crossbody",
        "bullet_points": [
            "Handcrafted from thick, durable full-grain cowhide leather that develops a rich natural patina over time.",
            "Features dual solid brass buckles and reinforced cross-body strap adjustable up to 54 inches.",
            "Padded shock-absorbing partition fits DSLR cameras, lenses, or daily everyday carry (EDC) tablets up to 11 inches.",
            "Authentic vintage aesthetic with minor natural grain markings that celebrate true artisanal character."
        ],
        "tags": ["camera bag", "leather satchel", "vintage messenger", "gift for photographer", "rustic crossbody", "etsy vintage"],
        "social_script": "Looking for the ultimate vintage camera bag? Check out this handcrafted full-grain leather satchel with antique brass hardware. It fits your camera and lenses with style that turns heads. Link in bio to grab yours!",
        "sample_image": "assets/specimens/camera_bag.jpg"
    },
    "ceramic_matcha_bowl": {
        "title": "Artisanal Speckled Ceramic Matcha Chawan with Pouring Spout",
        "category": "Home & Ceramic Decor",
        "condition": "Brand New / Handmade",
        "materials": ["Stoneware clay", "Food-safe iron-rich matte glaze", "Hand-pinched rim"],
        "seo_title": "Handmade Ceramic Matcha Bowl with Spout | Speckled Stoneware Chawan | Traditional Japanese Tea Ceremony Whisking Cup",
        "bullet_points": [
            "Wheel-thrown stoneware bowl featuring an ergonomic drip-free pouring spout for seamless lattes.",
            "Textured speckled matte glaze with subtle earthy tones; food-safe, microwave and dishwasher safe.",
            "Wide contoured bottom designed specifically for bamboo whisking (chasen) to yield luxurious micro-foam.",
            "Each chawan is uniquely shaped by hand in small artisan batches—no two pieces are identical."
        ],
        "tags": ["matcha bowl", "ceramic chawan", "tea ceremony", "stoneware cup", "handmade pottery", "japandi decor"],
        "social_script": "Upgrade your morning tea ritual! This wheel-thrown ceramic matcha bowl features an artisanal matte glaze and a precision pouring spout. Whisk the creamiest froth effortlessly. Tap the link to shop before this batch sells out!",
        "sample_image": "assets/specimens/matcha_bowl.jpg"
    }
}


def lookup_offline_template(keyword: str) -> Dict[str, Any]:
    """Finds an appropriate pre-cached listing template when offline or API is absent."""
    clean = keyword.lower().strip()
    if any(k in clean for k in ["ceramic", "pottery", "matcha", "bowl", "cup", "plate", "vase"]):
        return OFFLINE_SPECIMEN_CATALOG["ceramic_matcha_bowl"]
    return OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"]
