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
from src.compliance_scanner import scan_trademark_compliance
from src.localizer import localize_listing, FX_RATES

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
    env_gemini = os.getenv("GEMINI_API_KEY", "")
    env_eleven = os.getenv("ELEVENLABS_API_KEY", "")

    if env_gemini:
        st.success("🔒 Cloud Gemini Key: Configured & Secured")
        user_override_gemini = st.text_input(
            "Custom Gemini Key (Optional Override)",
            value="",
            type="password",
            help="Your server key is already securely active. Leave empty to use the server key."
        )
        gemini_key = user_override_gemini if user_override_gemini.strip() else env_gemini
    else:
        gemini_key = st.text_input(
            "Google Gemini / Gemma API Key",
            value="",
            type="password",
            help="Enter your Google AI Studio key for Gemma 2. Falls back to offline mode if blank."
        )

    if env_eleven:
        st.success("🔒 Cloud ElevenLabs Key: Configured")
        user_override_eleven = st.text_input(
            "Custom ElevenLabs Key (Optional Override)",
            value="",
            type="password",
            help="Leave empty to use configured server key."
        )
        elevenlabs_key = user_override_eleven if user_override_eleven.strip() else env_eleven
    else:
        elevenlabs_key = st.text_input(
            "ElevenLabs API Key (Optional)",
            value="",
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📸 Multimodal Listing Generator",
    "🛡️ Trademark & IP Risk Scanner",
    "🌐 Cross-Border Multi-Language Hub",
    "📈 TabPFN Dynamic Pricing & Elasticity",
    "🎙️ Social Video Voiceover (TikTok/Reels)",
    "💼 Reseller ROI & CSV Exporter"
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

# ----------------- TAB 2: Trademark & IP Risk Scanner -----------------
with tab2:
    st.subheader("🛡️ Trademark & Marketplace IP Compliance Radar")
    st.caption("Scans listing copy against high-risk registered trademarks (e.g., Velcro, Onesie, Tiffany Blue) to protect side-hustlers from store bans.")

    active_for_scan = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
    combined_copy = f"{active_for_scan.get('seo_title', '')} {' '.join(active_for_scan.get('bullet_points', []))} {' '.join(active_for_scan.get('search_tags', []))}"
    
    test_text = st.text_area("Audit Copy for Intellectual Property Hazards:", value=combined_copy, height=110)
    
    col_sc1, col_sc2 = st.columns([1, 1])
    if col_sc1.button("🔍 Scan for Trademark Infringements", type="primary", use_container_width=True):
        st.session_state["compliance_scanned"] = True

    scan_result = scan_trademark_compliance(test_text)
    
    m_s1, m_s2 = st.columns(2)
    m_s1.metric("Compliance Health Score", f"{scan_result['compliance_score']}/100")
    m_s2.metric("Policy Status", "100% CLEAN" if scan_result['is_clean'] else "RISKS DETECTED")

    if scan_result["is_clean"]:
        st.success("✅ **Zero Trademark Infringements Found**: This listing is safe for commercial publishing on Etsy, eBay, and Amazon.")
    else:
        st.error(f"⚠️ **Attention**: Found {len(scan_result['violations'])} restricted commercial trademarks!")
        for viol in scan_result["violations"]:
            with st.expander(f"🚩 Restricted Term: '{viol['flagged_term']}' ({viol['risk_level']} RISK)"):
                st.markdown(f"- **Trademark Registered By**: `{viol['trademark_owner']}`")
                st.markdown(f"- **Recommended Safe Replacement**: `{viol['safe_replacement']}`")
                st.caption("Using this brand name without licensing can trigger automated DMCA takedowns.")

# ----------------- TAB 3: Cross-Border Multi-Language Hub -----------------
with tab3:
    st.subheader("🌐 Cross-Border Multi-Currency & Locale Localizer")
    st.caption("Expands your side hustle into lucrative European and Asian markets with localized titles and currency conversions.")

    loc_c1, loc_c2 = st.columns([1, 1])
    target_locale = loc_c1.selectbox("Target Global Market", ["German (DE - Etsy/eBay)", "French (FR - Etsy/eBay)", "Japanese (JP - Mercari/Rakuten)"])
    active_data_loc = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
    
    current_price_usd = 42.0

    if st.button("🌍 Translate & Localize for Global Buyers", type="primary", use_container_width=True):
        with st.spinner(f"Localizing for {target_locale}..."):
            localized = localize_listing(
                english_title=active_data_loc.get("seo_title", ""),
                english_bullets=active_data_loc.get("bullet_points", []),
                usd_price=current_price_usd,
                target_locale=target_locale,
                api_key=gemini_key
            )
            st.session_state["localized_data"] = localized

    loc_active = st.session_state.get("localized_data", None)
    if loc_active:
        curr_symbol = "€" if loc_active["currency"] == "EUR" else ("¥" if loc_active["currency"] == "JPY" else "£")
        st.success(f"Localized for **{loc_active['locale']}** | Converted Price: **{curr_symbol}{loc_active['local_price']} {loc_active['currency']}**")
        
        st.write("##### 🏷️ Localized Title:")
        st.code(loc_active.get("translated_title", ""), language="text")

        st.write("##### 📌 Culturally Adapted Bullet Points:")
        for b in loc_active.get("translated_bullets", []):
            st.markdown(f"- {b}")

        st.write("##### 🔍 Local Search Keywords:")
        st.code(", ".join(loc_active.get("local_tags", [])), language="text")
    else:
        st.info("👆 Select a global market and click 'Translate & Localize' to generate international sales copy.")

# ----------------- TAB 4: TabPFN Dynamic Pricing & Elasticity -----------------
with tab4:
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

# ----------------- TAB 5: Social Video Voiceover (TikTok/Reels) -----------------
with tab5:
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

# ----------------- TAB 6: Reseller ROI & CSV Bulk Exporter -----------------
with tab6:
    st.subheader("💼 Side Hustle Growth & CSV Bulk Exporter")
    st.caption("Compare solo manual listing hours vs. ListingCraft AI throughput, and export official Etsy/Shopify bulk upload CSVs.")

    calc_c1, calc_c2, calc_c3 = st.columns(3)
    monthly_items = calc_c1.slider("Monthly Sourced Items", 10, 300, 60, step=10)
    avg_sale_price = calc_c2.slider("Average Selling Price ($)", 15.0, 250.0, float(pricing_res['optimal_price']), step=5.0)
    avg_item_cost = calc_c3.slider("Average Sourcing Cost ($)", 2.0, 100.0, sourcing_cost, step=2.0)

    # Manual vs AI Time savings
    manual_hours = (monthly_items * 25.0) / 60.0
    ai_hours = (monthly_items * 3.0) / 60.0
    hours_saved = round(manual_hours - ai_hours, 1)

    monthly_rev = monthly_items * avg_sale_price
    platform_fee_total = monthly_rev * 0.13
    sourcing_total = monthly_items * avg_item_cost
    monthly_net_profit = monthly_rev - platform_fee_total - sourcing_total

    r1, r2, r3 = st.columns(3)
    r1.metric("Projected Monthly Revenue", f"${monthly_rev:,.2f}")
    r2.metric("Projected Monthly Net Profit", f"${monthly_net_profit:,.2f}", f"{(monthly_net_profit/max(1.0, monthly_rev))*100:.1f}% Margin")
    r3.metric("Time Saved with AI", f"{hours_saved} Hours/Mo", f"{(hours_saved/manual_hours)*100:.0f}% Faster")

    st.markdown("---")
    st.subheader("📦 Bulk Export Catalog (Etsy / Shopify CSV Format)")
    
    # Generate CSV payload
    csv_rows = [
        "Title,Description,Price,Quantity,Tags,Materials",
        f"\"{active_listing.get('seo_title', '')}\",\"{' '.join(active_listing.get('bullet_points', []))}\",{pricing_res['optimal_price']},1,\"{', '.join(active_listing.get('search_tags', []))}\",\"{', '.join(active_listing.get('detected_materials', []))}\""
    ]
    csv_payload = "\n".join(csv_rows)
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        st.download_button(
            "📊 Download Marketplace Bulk CSV",
            data=csv_payload,
            file_name=f"listingcraft_{target_platform.lower()}_catalog.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c_btn2:
        export_text_bundle = f"""=== LISTING CRAFT EXPORT ===
Platform: {target_platform}
Title: {active_listing.get('seo_title', '')}
Price: ${pricing_res['optimal_price']:.2f}
Tags: {', '.join(active_listing.get('search_tags', []))}
"""
        st.download_button(
            "📝 Download Full Text Package (.txt)",
            data=export_text_bundle,
            file_name="listingcraft_bundle.txt",
            mime="text/plain",
            use_container_width=True
        )
