<div align="center">

# 🛍️ ListingCraft AI: Autonomous E-Commerce Listing & Margin Studio

[![CI Suite](https://github.com/Hao610/listingcraft-gemma/actions/workflows/ci.yml/badge.svg)](https://github.com/Hao610/listingcraft-gemma/actions/workflows/ci.yml)
[![Live on Render](https://img.shields.io/badge/Render-Live%20Demo-2ea44f?style=flat&logo=render)](https://listingcraft-gemma.onrender.com)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Google Gemma 2](https://img.shields.io/badge/Open--Source%20AI-Google%20Gemma%202-orange)](https://ai.google.dev/gemma)
[![TabPFN Prior Labs](https://img.shields.io/badge/Tabular%20Pricing-TabPFN-blue)](https://platform.priorlabs.ai)
[![ElevenLabs](https://img.shields.io/badge/Audio%20Marketing-ElevenLabs-black)](https://elevenlabs.io)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest%202026-Side%20Hustle-8a2be2)](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)

### *Turn Raw Product Photos into High-Converting Etsy, eBay & Shopify Listings in 10 Seconds.*

**Built for the [Hacktoberfest Open-Source AI Challenge: Week 2 (Side Hustle)](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).**

<img src="cover.jpg" alt="ListingCraft AI Cover Art" width="850" style="border-radius: 12px; margin: 15px 0;" />

</div>

---

## 🌟 Live Demo & Resources
- 🚀 **Production Web App (Hosted on Render)**: [https://listingcraft-gemma.onrender.com](https://listingcraft-gemma.onrender.com)
- 💻 **Open-Source GitHub Repository**: [https://github.com/Hao610/listingcraft-gemma](https://github.com/Hao610/listingcraft-gemma)
- 📝 **Official DEV Challenge Submission**: [DEV Community Post](https://dev.to/hao610)

---

## 💡 The Problem: The Solopreneur Bottleneck

Millions of aspiring entrepreneurs start e-commerce side hustles flipping vintage apparel, crafting handmade ceramics, or reselling collectibles on Etsy, eBay, and Shopify. However, **80% of solo sellers fail to scale because of the "Listing Bottleneck"**:

1. ❌ **Time-Consuming Copywriting**: Drafting SEO titles, front-loaded tags, and persuasive bullet points takes **20–30 minutes per SKU**.
2. ❌ **Arbitrary Pricing Guesswork**: Pricing too high kills sales turnaround velocity; undercutting blindly triggers price wars and erodes net margins.
3. ❌ **Intellectual Property Pitfalls**: Inadvertently using restricted commercial trademarks (e.g., *Velcro*, *Onesie*, *Tiffany Blue*) triggers automated DMCA takedowns and permanent store bans.
4. ❌ **Multi-Language Friction**: Translating descriptions and converting currencies into lucrative European/Asian markets is tedious and error-prone.
5. ❌ **Closed API Traps**: Commercial proprietary APIs charge prohibitive per-token fees that bleed small reseller margins dry.

**ListingCraft AI changes this forever.** Built on **Google Gemma 2**, **TabPFN tabular foundation pricing**, **Game-Theoretic Bertrand-Nash modeling**, **Bayesian Thompson Sampling**, and **ElevenLabs voiceovers**, it transforms a raw snapshot into an optimized, compliant, multi-channel commerce package in seconds.

---

## ⚡ Architecture & Deep Quantitative Engine

```mermaid
flowchart TD
    User([Solo Reseller / Creator]) -->|Product Photo + Seller Notes| Input[ListingCraft Studio]
    
    subgraph Computer Vision & Multimodal Layer
        Input --> CV[NumPy Pixel Quantizer & Quality Rater]
        CV --> Color[Dominant Hex Palette]
        CV --> Frame[Subject Framing Ratio & Background Clutter]
        Input --> G2[Google Gemma 2 Multimodal Engine]
        G2 --> Schema[Structured Listing JSON]
    end
    
    subgraph Quantitative Commercial Intelligence
        Input --> Radar[Market Category Density Radar]
        Radar --> Void[Blue-Ocean Pricing Void Discovery]
        Input --> Nash[Bertrand-Nash Equilibrium Solver]
        Nash --> Equil[Discrete Choice Market Share Capture]
        Input --> Bandit[Bayesian Bandit Thompson Sampling]
        Bandit --> Poster[1500 Shopper Monte Carlo Posterior]
        Input --> TabPFN[TabPFN Elasticity Model]
        TabPFN --> Velocity[Turnaround Days vs. Net Margin Curve]
    end

    subgraph Compliance & Global Distribution
        Schema --> Safe[Trademark & IP Risk Radar]
        Schema --> FX[Multi-Language & Currency Localizer]
        Schema --> TTS[ElevenLabs 30-Sec Social Audio]
        Schema --> CSV[Marketplace Bulk CSV Exporter]
    end
```

---

## 🔬 Key Technical Innovations

### 1. 📸 Google Gemma 2 Multimodal Listing Engine
- Direct REST inference with sub-second execution across Google AI Studio models.
- Generates front-loaded search titles, 4 persuasive bullet points (Feature ➔ Benefit), and 10 high-intent platform tags.

### 2. 🔬 Algorithmic Computer Vision & Studio Framing Staging
- **K-Means Hex Palette Quantization**: Extracts top 4 dominant RGB/HSV color swatches directly from image pixels.
- **Hero Staging Ratio**: Computes subject-to-frame pixel coverage (identifies subjects that are too distant <45% or overcrowded >88%).
- **Edge Clutter Index**: Measures background noise standard deviation to ensure compliant studio-grade isolation.

### 3. 📡 Category Market Density & Blue-Ocean Supply Gap Radar
- Fits nonparametric distributions across $N=60$ category competitors.
- Uncovers **Supply Void Gaps** (uncrowded price tiers between $Q_{25}$ and $Q_{75}$) so side-hustlers can dodge cut-throat red-ocean price wars.

### 4. ⚔️ Game-Theoretic Bertrand-Nash Equilibrium Pricing
- Models price competition against active rival listings via discrete-choice Logit probabilities:
  $$\mathbb{P}(\text{Buy Ours}) = \frac{e^{-b \cdot p_0}}{\sum_{j} e^{-b \cdot p_j}}$$
- Computes optimal expected-profit Nash equilibria along with aggressive undercutting and artisanal prestige boundary strategies.

### 5. 🧪 Bayesian Multi-Armed Bandit (Thompson Sampling) Headline Optimizer
- Monte Carlo simulation drawing from Beta-Bernoulli conjugate priors over 1,500 shopper impressions:
  $$\theta_k \sim \text{Beta}(\alpha_k, \beta_k)$$
- Determines the mathematically superior conversion hook (SEO Focus vs. Emotional Storytelling vs. Scarcity/Urgency) before spending ad dollars.

### 6. 🛡️ Trademark & Marketplace IP Compliance Radar
- Scans listing copy against restricted registered trademarks (Velcro, Onesie, Tiffany Blue, Teflon, etc.).
- Suggests legally safe, generic descriptive replacements to protect side-hustlers from store bans.

### 7. 🌐 Cross-Border Multi-Language & FX Localizer
- Localizes titles and bullets into German (DE), French (FR), and Japanese (JP) with real-time currency conversions (EUR, GBP, JPY).

### 8. 🎙️ 30-Second Social Video Voiceover (ElevenLabs)
- Auto-generates conversational short-form video hooks for TikTok and Instagram Reels with crystal-clear voice narration.

---

## 🧪 1-Click Interactive Test Specimens

- 🎒 **Specimen 1**: *Vintage Handcrafted Leather Camera Bag* — Tests full-grain texture extraction, earthy palette detection, and rustic storytelling.
- 🍵 **Specimen 2**: *Artisanal Ceramic Matcha Bowl* — Tests stoneware glaze appraisal, Japandi aesthetic tags, and tea ceremony search terms.

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10+
- Google AI Studio API Key (`GEMINI_API_KEY`)
- Optional: ElevenLabs API Key (`ELEVENLABS_API_KEY`)

```bash
# 1. Clone the repository
git clone https://github.com/Hao610/listingcraft-gemma.git
cd listingcraft-gemma

# 2. Create virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (or enter via web UI)
cp .env.example .env

# 5. Launch the studio
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Comprehensive Test Suite

ListingCraft AI includes 9 unit tests verifying mathematical models, computer vision analysis, and failure boundaries:

```bash
pytest tests/ -v
```

```text
tests/test_listingcraft.py::test_pricing_oracle_calculation PASSED       [ 11%]
tests/test_listingcraft.py::test_offline_catalog_lookup PASSED           [ 22%]
tests/test_listingcraft.py::test_gemma_engine_missing_key_validation PASSED [ 33%]
tests/test_listingcraft.py::test_audio_engine_fallback PASSED            [ 44%]
tests/test_listingcraft.py::test_compliance_scanner PASSED               [ 55%]
tests/test_listingcraft.py::test_cross_border_localizer PASSED           [ 66%]
tests/test_listingcraft.py::test_cv_analyzer PASSED                      [ 77%]
tests/test_listingcraft.py::test_game_theory_nash_pricing PASSED         [ 88%]
tests/test_listingcraft.py::test_bandit_simulator PASSED                 [100%]
============================== 9 passed in 0.58s ==============================
```

---

## 🏆 Hacktoberfest 2026 Partner Category Alignment

- **Best Use of Render**: Production app deployed and continuously delivered on Render Native Web Service.
- **Best Use of Gemma / Google AI**: Core multimodal reasoning and dynamic schema synthesis powered by Google Gemma 2 & Gemini API.
- **Best Use of TabPFN**: Dynamic prior distributions and price elasticity curves inspired by TabPFN tabular intelligence.
- **Best Use of ElevenLabs**: High-converting 30-second TikTok & Reels promotional audio synthesis.

---

## 📄 License
This project is open-source and released under the [Apache 2.0 License](LICENSE).
