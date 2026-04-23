import streamlit as st

COLORS = {
    "background": "#FDF6F0",
    "card": "#FFFFFF",
    "rose": "#C97D6E",
    "gold": "#D4A853",
    "sage": "#7E9B8A",
    "amber": "#E8A838",
    "green": "#7BAF7B",
    "text": "#3D2B1F",
    "muted": "#8C6E5D",
    "divider": "#EDD9CC",
    "partner1": "#C97D6E",
    "partner2": "#7E9B8A",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Helvetica Neue', sans-serif !important;
    color: #3D2B1F;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #3D2B1F;
    letter-spacing: -0.01em;
}

/* Main container padding */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 760px;
}

/* Text areas */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #EDD9CC !important;
    background: #FFFAF7 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    color: #3D2B1F !important;
    padding: 0.8rem 1rem !important;
}
.stTextArea textarea:focus {
    border-color: #C97D6E !important;
    box-shadow: 0 0 0 2px rgba(201,125,110,0.15) !important;
}

/* Text inputs */
.stTextInput input {
    border-radius: 12px !important;
    border: 1.5px solid #EDD9CC !important;
    background: #FFFAF7 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    color: #3D2B1F !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #C97D6E !important;
    box-shadow: 0 0 0 2px rgba(201,125,110,0.15) !important;
}

/* Primary buttons */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, #C97D6E 0%, #D4A853 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 28px !important;
    padding: 0.65rem 2.2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: opacity 0.2s ease, transform 0.1s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary / muted buttons */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #8C6E5D !important;
    border: 1.5px solid #EDD9CC !important;
    border-radius: 28px !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] {
    padding-top: 0.5rem;
}
.stSlider [data-testid="stThumbValue"] {
    font-family: 'Inter', sans-serif !important;
    color: #C97D6E !important;
    font-weight: 600;
}

/* Multiselect */
.stMultiSelect [data-baseweb="select"] {
    border-radius: 12px !important;
}

/* Radio buttons */
.stRadio [data-testid="stWidgetLabel"] {
    font-family: 'Inter', sans-serif !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #C97D6E, #D4A853) !important;
    border-radius: 4px !important;
}

/* Hide default streamlit footer/menu for cleanliness */
#MainMenu, footer, header { visibility: hidden; }

/* Custom card class */
.us-card {
    background: white;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    box-shadow: 0 2px 16px rgba(61, 43, 31, 0.07);
    margin-bottom: 1.2rem;
}

.us-pillar-card {
    background: white;
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 16px rgba(61, 43, 31, 0.07);
    margin-bottom: 1rem;
}

.us-pillar-card-attention {
    background: #FFFBF0;
    border: 1.5px solid #E8A838;
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
}

.us-pillar-card-good {
    background: #F4FAF4;
    border: 1.5px solid #7BAF7B;
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
}

.us-divider {
    border: none;
    border-top: 1.5px solid #EDD9CC;
    margin: 1.5rem 0;
}

.us-badge-p1 {
    display: inline-block;
    background: #F9EAE7;
    color: #C97D6E;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.03em;
}

.us-badge-p2 {
    display: inline-block;
    background: #E8F2EE;
    color: #5A8070;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.03em;
}

.us-action-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #3D2B1F;
}

.us-insight-card {
    background: linear-gradient(135deg, #F9EAE7 0%, #F3E8DF 100%);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #5A3A2B;
}

.us-score-low { color: #E8A838; font-weight: 600; }
.us-score-high { color: #7BAF7B; font-weight: 600; }
.us-score-mid  { color: #8C6E5D; }

.us-checkin-stale {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: #B09080;
    margin-top: 0.2rem;
}
"""


def inject():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def card_open(extra_class: str = "") -> None:
    st.markdown(f'<div class="us-card {extra_class}">', unsafe_allow_html=True)


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def divider() -> None:
    st.markdown('<hr class="us-divider">', unsafe_allow_html=True)


def badge(name: str, slot: str) -> str:
    cls = "us-badge-p1" if slot == "partner1" else "us-badge-p2"
    return f'<span class="{cls}">{name}</span>'


def action_bullet(text: str) -> str:
    return f'<div class="us-action-item"><span style="color:#C97D6E;margin-top:2px">✦</span><span>{text}</span></div>'


def insight_card(text: str) -> None:
    st.markdown(f'<div class="us-insight-card">💡 {text}</div>', unsafe_allow_html=True)
