"""
Comprehensive unit test suite for ListingCraft AI.
Tests TabPFN pricing oracle, offline catalog fallbacks, and audio synthesis engine.
"""

import pytest
from src.pricing_oracle import predict_optimal_pricing
from src.catalog_db import lookup_offline_template, OFFLINE_SPECIMEN_CATALOG
from src.gemma_engine import generate_listing_multimodal
from src.audio_engine import synthesize_marketing_audio


def test_pricing_oracle_calculation():
    """Verify TabPFN tabular pricing calculations and profit margins."""
    res = predict_optimal_pricing(
        category="Vintage Clothing",
        condition="Very Good (Minor Wear)",
        acquisition_cost=15.0,
        platform="Etsy",
        has_box_or_tags=False
    )
    assert res["optimal_price"] > 30.0
    assert res["net_profit"] > 0
    assert res["profit_margin_pct"] > 0
    assert len(res["elasticity_curve"]) == 5
    assert res["velocity_days_to_sell"] >= 1


def test_offline_catalog_lookup():
    """Verify deterministic fallback when querying offline keywords."""
    bag = lookup_offline_template("leather camera bag vintage")
    assert "Camera" in bag["title"]
    assert len(bag["bullet_points"]) == 4

    bowl = lookup_offline_template("ceramic matcha bowl stoneware")
    assert "Matcha" in bowl["title"]
    assert len(bowl["tags"]) > 3


def test_gemma_engine_missing_key_validation():
    """Verify multimodal engine enforces real dynamic API inference and rejects missing keys."""
    import pytest
    with pytest.raises(ValueError) as excinfo:
        generate_listing_multimodal(
            query_description="Handmade ceramic mug with blue glaze",
            image=None,
            category="Home & Ceramic Decor",
            condition="Brand New / Handmade",
            target_platform="Etsy",
            api_key=""
        )
    assert "API Key is missing" in str(excinfo.value)


def test_audio_engine_fallback():
    """Verify audio engine degrades gracefully without ElevenLabs key."""
    audio_bytes, msg = synthesize_marketing_audio("Check out this vintage bag!", api_key=None)
    assert audio_bytes is None
    assert "browser speech synthesis" in msg


def test_compliance_scanner():
    """Verify trademark scanning detects prohibited commercial terms."""
    from src.compliance_scanner import scan_trademark_compliance
    # Clean text
    clean_res = scan_trademark_compliance("Handcrafted leather satchel with brass zipper")
    assert clean_res["is_clean"] is True
    assert clean_res["compliance_score"] == 100

    # Infringing text (Velcro, Onesie)
    risky_res = scan_trademark_compliance("Cute baby onesie with velcro fasteners")
    assert risky_res["is_clean"] is False
    assert len(risky_res["violations"]) == 2
    assert risky_res["compliance_score"] < 100


def test_cross_border_localizer():
    """Verify German/French localization and foreign exchange conversion."""
    from src.localizer import localize_listing
    de_res = localize_listing("Vintage Leather Bag", ["Quality leather"], 50.0, "German (DE)", api_key="")
    assert de_res["currency"] == "EUR"
    assert de_res["local_price"] == 46.0
    assert len(de_res["translated_bullets"]) > 0


def test_cv_analyzer():
    """Verify computer vision color quantization and aspect ratio checks."""
    from src.cv_analyzer import analyze_product_image_cv
    from PIL import Image
    test_img = Image.new("RGB", (1200, 900), color=(140, 90, 60))
    res = analyze_product_image_cv(test_img)
    assert res["aspect_ratio"] == 1.33
    assert res["is_etsy_compliant_ratio"] is True
    assert len(res["dominant_palette"]) > 0


def test_game_theory_nash_pricing():
    """Verify Bertrand-Nash equilibrium pricing solver."""
    from src.game_theory import solve_bertrand_nash_equilibrium
    nash = solve_bertrand_nash_equilibrium(our_cost=15.0, competitor_prices=[35.0, 45.0, 60.0])
    assert nash["nash_equilibrium_price"] > 20.0
    assert nash["expected_market_share_pct"] > 0.0
    assert nash["aggressive_price"] < nash["artisan_premium_price"]


def test_bandit_simulator():
    """Verify Bayesian Thompson Sampling Multi-Armed Bandit simulation."""
    from src.bandit_simulator import run_thompson_sampling_simulation
    sim = run_thompson_sampling_simulation(
        variants=[{"label": "A", "text": "SEO"}, {"label": "B", "text": "Story"}],
        total_impressions=500
    )
    assert sim["total_simulated_impressions"] == 500
    assert len(sim["arm_results"]) == 2
    assert sim["champion_win_probability"] > 0.0
