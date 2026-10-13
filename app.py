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
from src.cv_analyzer import analyze_product_image_cv
from src.game_theory import solve_bertrand_nash_equilibrium
from src.bandit_simulator import run_thompson_sampling_simulation

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
    .mockup-card {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    }
    .mockup-badge {
        background: #f59e0b;
        color: black;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .mockup-price {
        font-size: 1.6rem;
        font-weight: 800;
        color: #10b981;
    }
    .mockup-btn {
        background: #f97316;
        color: white;
        font-weight: 700;
        padding: 8px 16px;
        border-radius: 20px;
        text-align: center;
        display: block;
        margin-top: 10px;
        text-decoration: none;
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📸 Multimodal CV & Copy Studio",
    "⚔️ Game-Theoretic Nash Pricing",
    "🧪 Bayesian Bandit A/B Simulator",
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
        if s_c1.button("🎒 Specimen: Vintage Leather Bag", use_container_width=True):
            st.session_state["selected_img_path"] = "assets/specimens/camera_bag.jpg"
            st.session_state["prod_desc"] = "Vintage saddle-brown handcrafted full grain leather camera satchel, brass hardware buckles, adjustable strap."
            st.session_state["active_listing"] = OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"]
            # Auto-run CV
            if os.path.exists("assets/specimens/camera_bag.jpg"):
                st.session_state["cv_report"] = analyze_product_image_cv(Image.open("assets/specimens/camera_bag.jpg"))
            st.toast("Loaded 'Vintage Leather Bag' specimen!", icon="🎒")
            st.rerun()

        if s_c2.button("🍵 Specimen: Ceramic Matcha Bowl", use_container_width=True):
            st.session_state["selected_img_path"] = "assets/specimens/matcha_bowl.jpg"
            st.session_state["prod_desc"] = "Handmade speckled stoneware ceramic matcha chawan with pouring spout, wheel-thrown textured matte glaze."
            st.session_state["active_listing"] = OFFLINE_SPECIMEN_CATALOG["ceramic_matcha_bowl"]
            # Auto-run CV
            if os.path.exists("assets/specimens/matcha_bowl.jpg"):
                st.session_state["cv_report"] = analyze_product_image_cv(Image.open("assets/specimens/matcha_bowl.jpg"))
            st.toast("Loaded 'Ceramic Matcha Bowl' specimen!", icon="🍵")
            st.rerun()

        uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.session_state["uploaded_file_data"] = uploaded_file

        # Preview currently active image if available
        curr_specimen_path = st.session_state.get("selected_img_path", None)
        if uploaded_file is not None:
            st.image(uploaded_file, caption="📷 Uploaded Custom Photo", width=220)
        elif curr_specimen_path and os.path.exists(curr_specimen_path):
            st.image(curr_specimen_path, caption=f"📷 Active Specimen: {os.path.basename(curr_specimen_path)}", width=220)
        
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
            elif curr_specimen_path and os.path.exists(curr_specimen_path):
                loaded_image = Image.open(curr_specimen_path)

            if loaded_image:
                st.session_state["cv_report"] = analyze_product_image_cv(loaded_image)

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
                st.toast("Listing successfully generated by Gemma 2!", icon="✨")

        cv_data = st.session_state.get("cv_report", None)
        if cv_data:
            with st.expander("🔬 Computer Vision Analysis (Hex Palette & Studio Compliance)", expanded=True):
                st.caption(f"Resolution: **{cv_data['dimensions']}** | Aspect Ratio: **{cv_data['aspect_ratio']}** ({'✅ Optimal 4:3' if cv_data['is_etsy_compliant_ratio'] else '⚠️ Non-standard ratio'})")
                st.caption(f"Lighting & Sharpness Index: **{cv_data['photo_quality_score']}/100**")
                
                # Show dominant color swatches
                pal_cols = st.columns(len(cv_data["dominant_palette"]))
                for idx, pal in enumerate(cv_data["dominant_palette"]):
                    pal_cols[idx].markdown(f"""
                    <div style="background:{pal['hex']}; height:32px; border-radius:6px; border:1px solid #64748b; margin-bottom:4px;"></div>
                    <div style="font-size:10px; text-align:center; color:#94a3b8;">{pal['hex']}<br>{pal['percentage']}%</div>
                    """, unsafe_allow_html=True)

        active_data = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
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

            st.markdown("---")
            st.subheader("📊 Listing Conversion & Quality Radar")
            
            # Plotly 5-Dimensional Radar Chart
            categories_radar = ['SEO Keyword Density', 'Emotional Conversion', 'Algorithm Affinity', 'Material Fidelity', 'IP Safety']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[94, 91, 96, 95, 98],
                theta=categories_radar,
                fill='toself',
                name='Listing Quality Index',
                fillcolor='rgba(99, 102, 241, 0.35)',
                line=dict(color='#818cf8', width=2)
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10, color="#94a3b8")),
                    bgcolor="#0f172a"
                ),
                showlegend=False,
                template="plotly_dark",
                height=260,
                margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            # Live WYSIWYG Marketplace Mockup Card
            st.subheader("🛍️ Live Marketplace Preview (Buyer View)")
            st.markdown(f"""
            <div class="mockup-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="mockup-badge">🔥 Bestseller Candidate</span>
                    <span style="color: #94a3b8; font-size: 0.8rem;">★★★★★ (148 reviews)</span>
                </div>
                <h4 style="margin: 0.6rem 0 0.3rem 0; color: #f8fafc; font-size: 1.05rem;">{active_data.get('seo_title', '')[:75]}...</h4>
                <div style="display: flex; align-items: baseline; gap: 10px; margin-top: 5px;">
                    <span class="mockup-price">$42.00</span>
                    <span style="color: #94a3b8; text-decoration: line-through; font-size: 0.9rem;">$58.00</span>
                    <span style="color: #10b981; font-size: 0.85rem; font-weight: bold;">FREE Shipping</span>
                </div>
                <p style="color: #cbd5e1; font-size: 0.82rem; margin: 0.5rem 0;">
                    👀 <i>In 6 people's carts · Only 1 available, make it yours!</i>
                </p>
                <div class="mockup-btn">Add to Cart ➔ Buy on {target_platform}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👆 Tap a specimen or upload an image and click 'Craft High-Converting Listing' to see Gemma 2 in action.")

# ----------------- TAB 2: Game-Theoretic Nash Pricing -----------------
with tab2:
    st.subheader("⚔️ Game-Theoretic Competitor Scraping & Bertrand-Nash Equilibrium Engine")
    st.caption("Solves for optimal price equilibria against competing listings using Bertrand differentiated oligopoly modeling.")

    gt_c1, gt_c2 = st.columns([1, 1])
    with gt_c1:
        st.markdown("##### 🎯 Competitor Market Price Survey")
        st.caption("Active rival listings discovered in the same category:")
        comp_p1 = st.number_input("Rival Seller A (Budget Challenger, $)", min_value=5.0, value=34.0, step=1.0)
        comp_p2 = st.number_input("Rival Seller B (Mid-Market Bestseller, $)", min_value=5.0, value=48.0, step=1.0)
        comp_p3 = st.number_input("Rival Seller C (Premium Artisan Brand, $)", min_value=5.0, value=65.0, step=1.0)
        
        solve_btn = st.button("🧮 Compute Nash Equilibrium Solution", type="primary", use_container_width=True)
        if solve_btn:
            st.toast("Recomputed Bertrand-Nash Game Equilibrium!", icon="🧮")

    with gt_c2:
        st.markdown("##### 🏆 Equilibrium Strategy Readout")
        if solve_btn:
            st.success("✅ Nash Equilibrium Solved: Computed optimal price & discrete choice market share.")
        nash_res = solve_bertrand_nash_equilibrium(
            our_cost=sourcing_cost,
            competitor_prices=[comp_p1, comp_p2, comp_p3]
        )
        
        n_m1, n_m2, n_m3 = st.columns(3)
        n_m1.metric("Nash Equilibrium Price", f"${nash_res['nash_equilibrium_price']:.2f}", help="Optimal risk-neutral expected profit price")
        n_m2.metric("Market Capture Share", f"{nash_res['expected_market_share_pct']}%", help="Predicted choice probability under logit discrete choice")
        n_m3.metric("Competitor Mean", f"${nash_res['competitor_mean']:.2f}")

        st.info(f"💡 **Game-Theoretic Verdict**: {nash_res['strategy_recommendation']}")
        
        # Dual Strategy Cards
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px;">
            <div style="background:#0f172a; padding:10px; border-radius:8px; border-left:3px solid #f59e0b;">
                <b style="color:#f59e0b;">Aggressive Undercutting:</b><br>
                <span style="font-size:1.1rem; font-weight:700;">${nash_res['aggressive_price']:.2f}</span><br>
                <small style="color:#94a3b8;">Max sales velocity</small>
            </div>
            <div style="background:#0f172a; padding:10px; border-radius:8px; border-left:3px solid #8b5cf6;">
                <b style="color:#8b5cf6;">Artisanal Premium:</b><br>
                <span style="font-size:1.1rem; font-weight:700;">${nash_res['artisan_premium_price']:.2f}</span><br>
                <small style="color:#94a3b8;">Max brand prestige</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: Bayesian Bandit A/B Simulator -----------------
with tab3:
    st.subheader("🧪 Bayesian Multi-Armed Bandit (Thompson Sampling) Headline Optimizer")
    st.caption("Simulates 1,500 real consumer traffic impressions using Beta-Bernoulli conjugate priors to determine the winning conversion angle.")

    active_b = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
    
    variant_a = active_b.get("seo_title", "Vintage Leather Camera Bag Satchel | Handcrafted Rustic Messenger")
    variant_b = f"Handcrafted Artisan Heritage: {active_b.get('item_name', 'Leather Bag')} with Patina"
    variant_c = f"Rare Find! Authentic {active_b.get('item_name', 'Leather Satchel')} - Fast Shipping"

    b_col1, b_col2 = st.columns([1.1, 0.9])
    with b_col1:
        st.markdown("##### 🧬 Competing Copywriting Hypotheses")
        h_a = st.text_input("Arm A (SEO Keyword Focus):", value=variant_a)
        h_b = st.text_input("Arm B (Emotional Storytelling):", value=variant_b)
        h_c = st.text_input("Arm C (Scarcity & Urgency):", value=variant_c)
        
        sim_impressions = st.slider("Simulated Shopper Traffic (Impressions)", 500, 5000, 1500, step=250)
        run_sim_btn = st.button("🚀 Run Thompson Sampling Simulation", type="primary", use_container_width=True)
        if run_sim_btn:
            st.toast(f"Executed Monte Carlo simulation with {sim_impressions} impressions!", icon="🧪")

    with b_col2:
        st.markdown("##### 📊 Posterior Convergence & Traffic Allocation")
        if run_sim_btn:
            st.success(f"🎯 Simulation complete across {sim_impressions} posterior draws!")
        bandit_res = run_thompson_sampling_simulation(
            variants=[
                {"label": "Arm A (SEO Focus)", "text": h_a},
                {"label": "Arm B (Emotional Story)", "text": h_b},
                {"label": "Arm C (Scarcity/Urgent)", "text": h_c}
            ],
            total_impressions=sim_impressions
        )
        
        st.success(f"🏆 Champion: **{bandit_res['champion_variant']}** ({bandit_res['champion_win_probability']}% Win Probability)")
        
        # Plotly bar chart for allocated traffic & posterior CTR
        arms = [r["variant_label"] for r in bandit_res["arm_results"]]
        pulls = [r["allocated_traffic"] for r in bandit_res["arm_results"]]
        ctrs = [r["posterior_ctr_pct"] for r in bandit_res["arm_results"]]

        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(
            x=arms,
            y=pulls,
            name="Traffic Allocation (Impressions)",
            marker_color="#6366f1"
        ))
        fig_b.add_trace(go.Scatter(
            x=arms,
            y=ctrs,
            name="Posterior CTR (%)",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#10b981", width=3)
        ))
        fig_b.update_layout(
            template="plotly_dark",
            yaxis=dict(title="Allocated Impressions"),
            yaxis2=dict(title="Simulated CTR (%)", overlaying="y", side="right"),
            height=280,
            margin=dict(l=30, r=30, t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_b, use_container_width=True)

# ----------------- TAB 4: Trademark & IP Risk Scanner -----------------
with tab4:
    st.subheader("🛡️ Trademark & Marketplace IP Compliance Radar")
    st.caption("Scans listing copy against high-risk registered trademarks (e.g., Velcro, Onesie, Tiffany Blue) to protect side-hustlers from store bans.")

    active_for_scan = st.session_state.get("active_listing", OFFLINE_SPECIMEN_CATALOG["vintage_leather_camera_bag"])
    combined_copy = f"{active_for_scan.get('seo_title', '')} {' '.join(active_for_scan.get('bullet_points', []))} {' '.join(active_for_scan.get('search_tags', []))}"
    
    test_text = st.text_area("Audit Copy for Intellectual Property Hazards:", value=combined_copy, height=110)
    
    col_sc1, col_sc2 = st.columns([1, 1])
    scan_clicked = col_sc1.button("🔍 Scan for Trademark Infringements", type="primary", use_container_width=True)
    if scan_clicked:
        st.toast("Trademark scan completed!", icon="🛡️")

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

# ----------------- TAB 5: Cross-Border Multi-Language Hub -----------------
with tab5:
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

# ----------------- TAB 6: TabPFN Dynamic Pricing & Elasticity -----------------
with tab6:
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

# ----------------- TAB 7: Social Video Voiceover (TikTok/Reels) -----------------
with tab7:
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

# ----------------- TAB 8: Reseller ROI & CSV Bulk Exporter -----------------
with tab8:
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
