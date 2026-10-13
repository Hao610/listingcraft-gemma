"""
ListingCraft AI - Autonomous Multimodal E-Commerce Listing & Pricing Studio
Built for Hacktoberfest 2026: Open-Source AI Challenge (Week 2: Side Hustle)
"""

import os
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from dotenv import load_dotenv

from src.gemma_engine import generate_listing_multimodal
from src.pricing_oracle import predict_optimal_pricing, CATEGORY_PRIORS, CONDITION_MULTIPLIERS
from src.audio_engine import synthesize_marketing_audio
from src.catalog_db import OFFLINE_SPECIMEN_CATALOG

load_dotenv()

st.set_page_config(
    page_title="ListingCraft AI | Autonomous E-Commerce Studio",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Converting SaaS Branding CSS
st.markdown("""
<style>
    .saas-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        color: #e0e7ff;
        padding: 1.5rem 1.8rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
        border: 1px solid #6366f1;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.25);
    }
    .saas-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.6px;
    }
    .saas-subtitle {
        font-size: 1.05rem;
        color: #c7d2fe;
        margin-top: 0.3rem;
    }
    .kpi-card {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .badge-roi {
        background-color: #10b981;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Header
st.markdown("""
<div class="saas-header">
    <div class="saas-title">🛍️ ListingCraft AI: The Side Hustle Listing & Margin Studio</div>
    <div class="saas-subtitle">Turn raw product photos into high-converting <b>Etsy, eBay & Shopify</b> listings using <b>Google Gemma 2</b>, <b>TabPFN Dynamic Pricing</b> & <b>ElevenLabs Audio Scripts</b>.</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Studio Settings & Keys")
    gemini_key = st.text_input(
        "Google Gemini / Gemma API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Google AI Studio key for Gemma 2 Multimodal reasoning. Falls back to offline templates if blank."
    )
    elevenlabs_key = st.text_input(
        "ElevenLabs API Key",
        value=os.getenv("ELEVENLABS_API_KEY", ""),
        type="password",
        help="Generates 30-sec social video marketing voiceovers. Falls back to browser audio."
    )

    st.markdown("---")
    st.subheader("🎯 Marketplace & Unit Economics")
    target_platform = st.selectbox("Target Marketplace", ["Etsy", "eBay", "Shopify"])
    product_category = st.selectbox("Product Category", list(CATEGORY_PRIORS.keys()))
    product_condition = st.selectbox("Item Condition", list(CONDITION_MULTIPLIERS.keys()))
    
    st.markdown("---")
    st.subheader("💰 Reseller Cost Structure")
    sourcing_cost = st.number_input("Item Acquisition Cost ($)", min_value=0.0, value=15.0, step=1.0,
                                    help="Thrift store purchase price, raw material cost, or wholesale cost.")
    has_box = st.checkbox("Includes Original Packaging / Tags (+12% Premium)", value=True)

    st.markdown("---")
    st.caption("🏆 Built for **Hacktoberfest 2026** DEV Challenge: Week 2 'Side Hustle'.")

# Top Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Multimodal Listing Generator",
    "📈 TabPFN Dynamic Pricing & Elasticity",
    "🎙️ Social Video Voiceover (TikTok/Reels)",
    "💼 Reseller ROI & Side Hustle Calculator"
])

# ----------------- TAB 1: Multimodal Listing Generator -----------------
with tab1:
    col_input, col_output = st.columns([1.05, 0.95])

    with col_input:
        st.subheader("📤 Product Photo & Inspection Notes")
        st.caption("Upload your product image or click a 1-click test specimen:")

        # 1-Click Specimen Buttons
        s_c1, s_c2 = st.columns(2)
        selected_img_path = None
        if s_c1.button("🎒 Specimen: Vintage Leather Bag", use_container_width=True):
            selected_img_path = "assets/specimens/camera_bag.jpg"
            st.session_state["prod_desc"] = "Vintage saddle-brown handcrafted full grain leather camera satchel, brass hardware buckles, adjustable strap."
        if s_c2.button("🍵 Specimen: Ceramic Matcha Bowl", use_container_width=True):
            selected_img_path = "assets/specimens/matcha_bowl.jpg"
            st.session_state["prod_desc"] = "Handmade speckled stoneware ceramic matcha chawan with pouring spout, wheel-thrown textured matte glaze."

        uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
        
        user_notes = st.text_area(
            "Product Details / Seller Notes:",
            value=st.session_state.get("prod_desc", "Vintage saddle-brown handcrafted full grain leather camera satchel, brass hardware buckles, adjustable strap, minor natural patina."),
            height=90
        )

        generate_btn = st.button("✨ Craft High-Converting Listing with Gemma 2", type="primary", use_container_width=True)

    with col_output:
        st.subheader("📋 Generated Optimized Listing")

        if generate_btn and user_notes:
            loaded_image = None
            if uploaded_file is not None:
                loaded_image = Image.open(uploaded_file)
            elif selected_img_path and os.path.exists(selected_img_path):
                loaded_image = Image.open(selected_img_path)

            if loaded_image:
                st.image(loaded_image, caption="Inspected Product Visual Specimen", width=280)

            with st.spinner("Analyzing visual craftsmanship via Google Gemma 2..."):
                listing_data = generate_listing_multimodal(
                    query_description=user_notes,
                    image=loaded_image,
                    category=product_category,
                    condition=product_condition,
                    target_platform=target_platform,
                    api_key=gemini_key
                )
                st.session_state["active_listing"] = listing_data

        active_data = st.session_state.get("active_listing", None)
        if active_data:
            st.markdown(f"**Item**: `{active_data.get('item_name', 'Artisan Item')}`")
            st.markdown(f"**Aesthetic Style**: `{active_data.get('aesthetic_style', 'Rustic')}`")
            st.markdown(f"**Target Buyer Persona**: `{active_data.get('target_buyer_persona', 'Etsy Shoppers')}`")
            
            st.write("##### 🏷️ SEO Optimized Title (Front-Loaded Keywords):")
            st.code(active_data.get("seo_title", ""), language="text")

            st.write("##### 📌 Persuasive Bullet Points (Feature ➔ Benefit):")
            for b in active_data.get("bullet_points", []):
                st.markdown(f"- {b}")

            st.write("##### 🔍 High-Intent Search Tags (Copy & Paste):")
            tag_str = ", ".join(active_data.get("search_tags", []))
            st.code(tag_str, language="text")
            st.caption(f"Engine: {active_data.get('engine', 'Gemma 2')}")
        else:
            st.info("👆 Tap a specimen or upload an image and click 'Craft High-Converting Listing' to see Gemma 2 in action.")

# ----------------- TAB 2: TabPFN Dynamic Pricing & Elasticity -----------------
with tab2:
    st.subheader("📈 TabPFN Tabular Prior Pricing & Elasticity Model")
    st.caption("Calculates optimal velocity price, clearance floor, and net margins based on market tabular distributions.")

    pricing_res = predict_optimal_pricing(
        category=product_category,
        condition=product_condition,
        acquisition_cost=sourcing_cost,
        platform=target_platform,
        has_box_or_tags=has_box
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Recommended List Price", f"${pricing_res['optimal_price']:.2f}", help="Sweet spot balancing velocity and profit")
    k2.metric("Estimated Net Profit", f"${pricing_res['net_profit']:.2f}", f"{pricing_res['roi_percent']}% ROI")
    k3.metric("Profit Margin", f"{pricing_res['profit_margin_pct']}%")
    k4.metric("Avg Velocity to Sell", f"{pricing_res['velocity_days_to_sell']} Days")

    # Plotly Price Elasticity Curve
    curve_data = pricing_res["elasticity_curve"]
    prices = [c["price"] for c in curve_data]
    days = [c["days_to_sell"] for c in curve_data]
    profits = [c["net_profit"] for c in curve_data]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"${p:.2f}" for p in prices],
        y=profits,
        name="Net Profit ($)",
        marker_color="#4f46e5",
        yaxis="y"
    ))
    fig.add_trace(go.Scatter(
        x=[f"${p:.2f}" for p in prices],
        y=days,
        name="Estimated Days to Sell",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=3),
        yaxis="y2"
    ))

    fig.update_layout(
        title="Price Elasticity vs. Turnaround Velocity (TabPFN Tabular Prior)",
        template="plotly_dark",
        xaxis_title="Listing Price Scenarios",
        yaxis=dict(title="Net Profit ($)", side="left"),
        yaxis2=dict(title="Days to Sell (Velocity)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
        height=360
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"💡 **Pricing Rationale**: {pricing_res['pricing_rationale']} (Premium Ceiling: **${pricing_res['premium_price']:.2f}** | Clearance Floor: **${pricing_res['clearance_floor']:.2f}**)")

# ----------------- TAB 3: Social Video Voiceover (TikTok/Reels) -----------------
with tab3:
    st.subheader("🎙️ 30-Second Social Commerce Voiceover Engine")
    st.caption("Generate natural, high-engagement TikTok and Instagram Reels audio scripts to drive viral traffic to your listings.")

    active_listing = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
    default_script = active_listing.get("social_video_script", "Check out this amazing find! Link in bio.")

    video_script = st.text_area("Voiceover Marketing Script (30 Seconds):", value=default_script, height=110)

    col_tts1, col_tts2 = st.columns([1, 1])
    with col_tts1:
        synth_btn = st.button("🎧 Synthesize Audio with ElevenLabs", use_container_width=True, type="primary")

    if synth_btn and video_script.strip():
        with st.spinner("Synthesizing audio voiceover..."):
            audio_bytes, audio_msg = synthesize_marketing_audio(video_script, api_key=elevenlabs_key)

        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            st.success(f"✨ {audio_msg}")
        else:
            st.warning(f"🔊 {audio_msg}")
            # Browser offline SpeechSynthesis fallback
            st.components.v1.html(f"""
            <script>
                if ('speechSynthesis' in window) {{
                    const utterance = new SpeechSynthesisUtterance({repr(video_script)});
                    utterance.rate = 1.05;
                    utterance.pitch = 1.0;
                    window.speechSynthesis.speak(utterance);
                }}
            </script>
            """, height=0)

# ----------------- TAB 4: Reseller ROI & Side Hustle Calculator -----------------
with tab4:
    st.subheader("💼 Side Hustle Growth & ROI Simulator")
    st.caption("Compare solo manual listing hours vs. ListingCraft AI automated throughput to project monthly side hustle earnings.")

    calc_c1, calc_c2, calc_c3 = st.columns(3)
    monthly_items = calc_c1.slider("Monthly Sourced Items", 10, 300, 60, step=10)
    avg_sale_price = calc_c2.slider("Average Selling Price ($)", 15.0, 250.0, float(pricing_res['optimal_price']), step=5.0)
    avg_item_cost = calc_c3.slider("Average Sourcing Cost ($)", 2.0, 100.0, sourcing_cost, step=2.0)

    # Manual vs AI Time savings
    manual_hours = (monthly_items * 25.0) / 60.0  # ~25 mins per listing manually
    ai_hours = (monthly_items * 3.0) / 60.0       # ~3 mins with ListingCraft
    hours_saved = round(manual_hours - ai_hours, 1)

    # Monthly revenue & profit
    monthly_rev = monthly_items * avg_sale_price
    platform_fee_total = monthly_rev * 0.13
    sourcing_total = monthly_items * avg_item_cost
    monthly_net_profit = monthly_rev - platform_fee_total - sourcing_total

    r1, r2, r3 = st.columns(3)
    r1.metric("Projected Monthly Revenue", f"${monthly_rev:,.2f}")
    r2.metric("Projected Monthly Net Profit", f"${monthly_net_profit:,.2f}", f"{(monthly_net_profit/max(1.0, monthly_rev))*100:.1f}% Margin")
    r3.metric("Time Saved with AI", f"{hours_saved} Hours/Mo", f"{(hours_saved/manual_hours)*100:.0f}% Faster")

    st.markdown("---")
    st.subheader("💾 Export Ready-to-Publish Listing Bundle")
    export_payload = f"""=== LISTING DATA (Generated by ListingCraft AI) ===
Platform: {target_platform}
Category: {product_category}
Condition: {product_condition}

OPTIMAL PRICE: ${pricing_res['optimal_price']:.2f} (Floor: ${pricing_res['clearance_floor']:.2f} | Premium: ${pricing_res['premium_price']:.2f})
PROJECTED NET PROFIT: ${pricing_res['net_profit']:.2f} ({pricing_res['roi_percent']}% ROI)

SEO TITLE:
{active_listing.get('seo_title', '')}

BULLET POINTS:
{chr(10).join(['- ' + b for b in active_listing.get('bullet_points', [])])}

SEARCH TAGS:
{', '.join(active_listing.get('search_tags', []))}

TIKTOK / REELS SCRIPT:
{active_listing.get('social_video_script', '')}
"""
    st.download_button(
        "📥 Download Listing Package (.txt)",
        data=export_payload,
        file_name=f"listingcraft_{target_platform.lower()}_bundle.txt",
        mime="text/plain",
        use_container_width=True
    )
