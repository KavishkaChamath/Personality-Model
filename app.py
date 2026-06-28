import os

import requests
import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Personality Predictor | Introvert vs Extrovert",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Futuristic CSS theme
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Rajdhani', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #0f1b2d 0%, #060a14 45%, #02040a 100%);
        color: #e8f1ff;
    }

    /* Hide default streamlit chrome */
    #MainMenu, header, footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        max-width: 760px;
    }

    /* Title */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00f5d4, #00bbf9, #9b5de5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 245, 212, 0.25);
        margin-bottom: 0.1rem;
        letter-spacing: 2px;
    }
    .neon-subtitle {
        text-align: center;
        color: #8fa3c2;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(0, 245, 212, 0.25);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45), inset 0 0 40px rgba(0, 245, 212, 0.03);
        backdrop-filter: blur(6px);
    }

    .section-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        color: #00f5d4;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        border-left: 3px solid #00f5d4;
        padding-left: 10px;
    }

    /* Sliders — make the full track visible on the dark background,
       then draw the filled portion in the neon gradient on top */
    div[data-baseweb="slider"] > div:first-of-type {
        background: rgba(255, 255, 255, 0.22) !important;
    }
    div[data-baseweb="slider"] > div:first-of-type > div {
        background: linear-gradient(90deg, #00f5d4, #00bbf9) !important;
    }
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #00f5d4 !important;
        box-shadow: 0 0 0 4px rgba(0, 245, 212, 0.25), 0 0 10px rgba(0, 245, 212, 0.8) !important;
    }
    /* Tick / min-max value labels under the slider */
    div[data-testid="stTickBar"] {
        color: #5d7390 !important;
    }

    /* Force readable colors regardless of viewer's/host's base theme */
    label, .stMarkdown, p, span,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #cdd9ec !important;
    }

    /* Number inputs (custom-value fields) */
    div[data-testid="stNumberInput"] input {
        background: #0c1626 !important;
        border: 1px solid rgba(0, 245, 212, 0.35) !important;
        border-radius: 10px !important;
        color: #e8f1ff !important;
        font-weight: 600;
        -webkit-text-fill-color: #e8f1ff !important;
    }
    div[data-testid="stNumberInput"] button {
        background: rgba(0, 245, 212, 0.12) !important;
        border: 1px solid rgba(0, 245, 212, 0.3) !important;
        color: #e8f1ff !important;
    }
    div[data-testid="stNumberInput"] svg {
        fill: #e8f1ff !important;
    }

    /* Slider current-value bubble */
    div[data-baseweb="slider"] div[data-testid="stTickBarMin"],
    div[data-baseweb="slider"] div[data-testid="stTickBarMax"] {
        color: #5d7390 !important;
    }
    div[data-testid="stSliderTickBarMin"],
    div[data-testid="stSliderTickBarMax"] {
        color: #5d7390 !important;
    }
    div[data-baseweb="slider"] + div {
        color: #00f5d4 !important;
    }

    /* Radio / toggle buttons */
    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,245,212,0.2);
        border-radius: 10px;
        padding: 4px 14px;
        margin-right: 8px;
        transition: all 0.2s ease;
    }

    /* Predict button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00f5d4, #00bbf9, #9b5de5);
        color: #021018;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        letter-spacing: 2px;
        border: none;
        border-radius: 14px;
        padding: 0.75rem 0;
        margin-top: 0.6rem;
        box-shadow: 0 0 25px rgba(0, 245, 212, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 0 40px rgba(0, 245, 212, 0.55);
        color: #021018;
    }

    /* Result card */
    .result-card {
        text-align: center;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        margin-top: 1.6rem;
        animation: fadeIn 0.6s ease;
    }
    .result-introvert {
        background: linear-gradient(135deg, rgba(155, 93, 229, 0.18), rgba(0, 187, 249, 0.10));
        border: 1px solid rgba(155, 93, 229, 0.45);
        box-shadow: 0 0 40px rgba(155, 93, 229, 0.25);
    }
    .result-extrovert {
        background: linear-gradient(135deg, rgba(0, 245, 212, 0.18), rgba(255, 200, 87, 0.10));
        border: 1px solid rgba(0, 245, 212, 0.45);
        box-shadow: 0 0 40px rgba(0, 245, 212, 0.25);
    }
    .result-emoji { font-size: 3.2rem; margin-bottom: 0.4rem; }
    .result-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: 3px;
        margin-bottom: 0.3rem;
    }
    .result-tier {
        font-size: 0.78rem;
        color: #8fa3c2;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.9rem;
        opacity: 0.85;
    }
    .result-desc { color: #b9c8e0; font-size: 0.95rem; max-width: 480px; margin: 0 auto; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .footer-note {
        text-align: center;
        color: #4f5f78;
        font-size: 0.78rem;
        margin-top: 2.5rem;
        letter-spacing: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Backend API config
# ----------------------------------------------------------------------------
# This Streamlit app is now a pure frontend — it sends inputs to the FastAPI
# service over HTTP and just displays the response. The model only lives
# behind the API.
#
# Set this to your deployed FastAPI URL (e.g. on Render). For local testing,
# run `uvicorn api:app --reload --port 8000` and leave the default below.
API_URL = os.environ.get("PERSONALITY_API_URL", "http://localhost:8000")

FEATURE_ORDER = [
    "Time_spent_Alone",
    "Stage_fear",
    "Social_event_attendance",
    "Going_outside",
    "Drained_after_socializing",
    "Friends_circle_size",
    "Post_frequency",
]

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="neon-title">PERSONALITY.AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="neon-subtitle">Neural Trait Analysis &nbsp;•&nbsp; Introvert / Extrovert Classifier</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Input form
# ----------------------------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Behavioral Signals</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    time_alone = st.slider("Time spent alone (hrs/day)", 0, 16, 4, 1)
    social_events = st.number_input(
        "Social event attendance (per month)", min_value=0, max_value=365, value=5, step=1
    )
    going_outside = st.slider("Going outside (days/week)", 0, 7, 4, 1)
with c2:
    friends_circle = st.number_input(
        "Friends circle size", min_value=0, max_value=1000, value=6, step=1
    )
    post_freq = st.number_input(
        "Social media post frequency (per week)", min_value=0, max_value=1000, value=4, step=1
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Psychological Indicators</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    stage_fear = st.radio("Stage fear?", ["No", "Yes"], horizontal=True)
with c4:
    drained = st.radio("Drained after socializing?", ["No", "Yes"], horizontal=True)

st.markdown("</div>", unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns([1, 1.4, 1])
with btn_col2:
    predict_clicked = st.button("⚡ ANALYZE PERSONALITY")

# ----------------------------------------------------------------------------
# Prediction
# ----------------------------------------------------------------------------
if predict_clicked:
    raw = {
        "Time_spent_Alone": time_alone,
        "Stage_fear": stage_fear,
        "Social_event_attendance": social_events,
        "Going_outside": going_outside,
        "Drained_after_socializing": drained,
        "Friends_circle_size": friends_circle,
        "Post_frequency": post_freq,
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=raw, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        st.error(
            f"Couldn't reach the prediction API at `{API_URL}`. "
            "Make sure the FastAPI service is running and reachable."
        )
        st.caption(f"Details: {e}")
        st.stop()

    label = result["prediction"]
    confidence_text = ""
    if result.get("confidence") is not None:
        confidence_text = f"Signal strength: {result['confidence']:.1f}%"

    is_introvert = str(label).lower().startswith("intro")

    # ------------------------------------------------------------------
    # Intensity tiers — the model only outputs Introvert/Extrovert, but
    # extreme raw inputs (e.g. almost no friends, no social events, lots
    # of time alone) describe a more withdrawn case than a "typical"
    # introvert, and vice-versa for extroverts. We tag that here purely
    # for the description text, using the raw (unencoded) inputs.
    # ------------------------------------------------------------------
    extreme_introvert = (
        raw["Time_spent_Alone"] >= 8
        and raw["Friends_circle_size"] <= 2
        and raw["Social_event_attendance"] <= 1
    )
    extreme_extrovert = (
        raw["Time_spent_Alone"] <= 1
        and raw["Friends_circle_size"] >= 10
        and raw["Social_event_attendance"] >= 8
    )

    if is_introvert and extreme_introvert:
        tier = "extreme_introvert"
    elif is_introvert:
        tier = "introvert"
    elif extreme_extrovert:
        tier = "extreme_extrovert"
    else:
        tier = "extrovert"

    TIER_INFO = {
        "extreme_extrovert": {
            "title": "Extreme Extrovert",
            "emoji": "🌟",
            "desc": (
                "Thrives on near-constant social stimulation and almost never seeks time alone. "
                "This can be a real strength in high-energy, people-facing settings — though "
                "deliberately carving out some quiet, reflective time now and then can help "
                "prevent burnout."
            ),
        },
        "extrovert": {
            "title": "Extrovert",
            "emoji": "☀️",
            "desc": (
                "Energized by social interaction, external stimulation, and active engagement "
                "with others."
            ),
        },
        "introvert": {
            "title": "Introvert",
            "emoji": "🌙",
            "desc": (
                "Recharges through solitude, reflection, and deep focus. Prefers smaller, "
                "meaningful interactions."
            ),
        },
        "extreme_introvert": {
            "title": "Extreme Introvert",
            "emoji": "🌑",
            "desc": (
                "Leans heavily toward isolation — very few social events, a tiny circle, and "
                "long stretches of time alone. A degree of solitude is healthy, but at this "
                "level it can drift from preference into withdrawal, so deliberately building "
                "in some regular, low-pressure social contact may genuinely help."
            ),
        },
    }

    css_class = "result-introvert" if is_introvert else "result-extrovert"
    emoji = TIER_INFO[tier]["emoji"]
    desc = TIER_INFO[tier]["desc"]
    intensity_tag = "Extreme pattern" if tier.startswith("extreme") else "Typical pattern"

    st.markdown(
        f"""
        <div class="result-card {css_class}">
            <div class="result-emoji">{emoji}</div>
            <div class="result-label">{label.upper()}</div>
            <div class="result-tier">{intensity_tag}</div>
            <div class="result-desc">{desc}</div>
            <div style="margin-top:0.8rem; color:#7d8fae; font-size:0.85rem;">{confidence_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer-note">MODEL: SUPPORT VECTOR MACHINE &nbsp;|&nbsp; TRAINED ON KAGGLE PERSONALITY DATASET</div>',
    unsafe_allow_html=True,
)
