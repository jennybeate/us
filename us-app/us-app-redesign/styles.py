"""
Drop-in replacement for styles.py.

Design goals (per the 'Improved' mockup):
- Less feminine, still warm. Rose -> clay (hue 55, chroma 0.08). Sage -> muted evergreen.
- No gradients on buttons. Solid ink button, hairline ghost button.
- Fraunces replaces Playfair (less 'wedding invitation'). Upright + medium weight,
  italic reserved for quiet voice only.
- JetBrains Mono tiny-caps for meta labels (phase, step counter, framework).
- Hairline rules replace drop-shadowed cards. Pillar rows, not pillar cards.

Backwards-compat notes:
- COLORS keys preserved ("partner1", "partner2", "rose", "gold", "sage", "amber",
  "green", "muted", "divider") so analysis.py, results.py, plotly traces, etc.
  keep working without changes. "rose" is now clay; "sage" is now evergreen.
- Legacy class names kept as aliases where other views reference them.
"""

import streamlit as st

# Concrete hex approximations of the oklch palette used in the mockup.
# (Streamlit can't do oklch in all contexts, so we bake to hex here.)
COLORS = {
    # Core neutrals
    "background": "#F7F3EC",   # warm off-white, slightly ochre
    "paper":      "#F1EBE0",   # card tint
    "card":       "#FFFFFF",   # kept for any view still asking for 'card'
    "ink":        "#2E261F",   # near-black, warm
    "text":       "#2E261F",   # alias
    "body":       "#5A4F46",   # body gray-brown
    "muted":      "#8B7F74",   # tertiary / meta
    "faint":      "#8B7F74",   # alias (was lighter before; unify)
    "divider":    "#DBD2C4",   # hairlines
    # Accents
    "clay":       "#B4704D",   # was 'rose'; warm clay
    "rose":       "#B4704D",   # alias — keep old key working
    "evergreen":  "#5B7A6E",   # was 'sage'; muted evergreen
    "sage":       "#5B7A6E",   # alias
    "gold":       "#B4704D",   # map to clay; we no longer mix two accents
    "amber":      "#B4704D",   # attention state shares clay
    "green":      "#5B7A6E",   # good state shares evergreen
    # Partner tints
    "partner1":    "#B4704D",
    "partner2":    "#5B7A6E",
    "p1_tint":     "#EFE1D6",
    "p2_tint":     "#DFE8E3",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Helvetica Neue', sans-serif !important;
    color: #2E261F;
    background: #F7F3EC;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-weight: 500;
    color: #2E261F;
    letter-spacing: -0.02em;
    font-style: normal;
}

/* Main container padding */
.main .block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 820px;
    background: #F7F3EC;
}

/* ── Meta label (tiny caps) ── */
.us-meta {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8B7F74;
    margin: 0;
}
.us-meta-ink  { color: #2E261F; }
.us-meta-clay { color: #B4704D; }
.us-meta-ever { color: #5B7A6E; }

/* ── Display type utilities ── */
.us-display {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    color: #2E261F;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.us-quiet {
    font-family: 'Fraunces', Georgia, serif;
    font-style: italic;
    color: #8B7F74;
}

/* ── Inputs: strip rounded/pill look; use hairline bottom rule ── */
.stTextArea textarea {
    border-radius: 2px !important;
    border: 1px solid #DBD2C4 !important;
    background: #FFFFFF !important;
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
    color: #2E261F !important;
    padding: 0.9rem 1rem !important;
}
.stTextArea textarea:focus {
    border-color: #2E261F !important;
    box-shadow: none !important;
}
.stTextInput input {
    border-radius: 2px !important;
    border: none !important;
    border-bottom: 1.5px solid #2E261F !important;
    background: transparent !important;
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 1.15rem !important;
    font-weight: 500 !important;
    color: #2E261F !important;
    padding: 0.5rem 0 !important;
}
.stTextInput input:focus {
    border-bottom-color: #B4704D !important;
    box-shadow: none !important;
}

/* ── Buttons: solid ink, hairline ghost — no gradients ── */
.stButton > button {
    background: #2E261F !important;
    color: #F7F3EC !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.75rem 1.6rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s ease !important;
    cursor: pointer !important;
    box-shadow: none !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: none !important; }
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #5A4F46 !important;
    border: 1px solid #DBD2C4 !important;
}

/* ── Sliders: thinner, ink-on-cream ── */
.stSlider [data-baseweb="slider"] { padding-top: 0.5rem; }
.stSlider [data-testid="stThumbValue"] {
    font-family: 'Fraunces', Georgia, serif !important;
    color: #B4704D !important;
    font-weight: 500 !important;
    font-size: 1.05rem !important;
}

/* ── Progress bar: single ink line, no gradient ── */
.stProgress > div > div {
    background: #2E261F !important;
    border-radius: 0 !important;
}
.stProgress > div {
    background: #DBD2C4 !important;
    border-radius: 0 !important;
    height: 1px !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── New structural elements ── */
.us-divider {
    border: none;
    border-top: 1px solid #DBD2C4;
    margin: 1.75rem 0;
}
.us-divider-strong {
    border: none;
    border-top: 1.5px solid #2E261F;
    margin: 1.75rem 0;
}

/* Pillar row (replaces pillar card) */
.us-pillar-row {
    padding: 1.75rem 0;
    border-top: 1px solid #DBD2C4;
}
.us-pillar-row-first { border-top: 1.5px solid #2E261F; }

/* State tags (inline text, not borders around cards) */
.us-tag-attn { color: #B4704D; font-weight: 500; }
.us-tag-good { color: #5B7A6E; font-weight: 500; }

/* Score bar (5 rectangles, no dots) */
.us-score-bar { display: inline-flex; gap: 3px; vertical-align: middle; }
.us-score-seg { width: 18px; height: 4px; border-radius: 1px; }

/* Numbered action list — user's own voice, Fraunces serif */
.us-action-list { margin: 0; padding: 0; list-style: none; }
.us-action-item {
    display: flex;
    gap: 0.65rem;
    padding: 0.55rem 0;
    border-top: 1px dashed #DBD2C4;
    font-family: 'Fraunces', Georgia, serif;
    font-size: 0.98rem;
    line-height: 1.55;
    color: #2E261F;
}
.us-action-item:first-child { border-top: none; }
.us-action-num {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.7rem;
    color: #8B7F74;
    min-width: 1.4rem;
    padding-top: 0.15rem;
    letter-spacing: 0.08em;
}

/* Insight panels (replaces gradient insight cards) */
.us-insight {
    border-top: 1.5px solid #2E261F;
    padding: 1.25rem 0 0.25rem;
    margin-bottom: 0.5rem;
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.1rem;
    line-height: 1.4;
    color: #2E261F;
    font-weight: 400;
}
.us-insight em, .us-insight strong {
    color: #B4704D;
    font-style: normal;
    font-weight: 500;
}

/* Partner badges (kept API, restyled to hairline pills) */
.us-badge-p1, .us-badge-p2 {
    display: inline-block;
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 2px;
    background: transparent;
}
.us-badge-p1 { color: #B4704D; border: 1px solid #B4704D; }
.us-badge-p2 { color: #5B7A6E; border: 1px solid #5B7A6E; }

/* ── Legacy class aliases: keep other views rendering ── */
.us-card,
.us-pillar-card,
.us-pillar-card-attention,
.us-pillar-card-good {
    background: transparent;
    padding: 1.25rem 0;
    border-top: 1px solid #DBD2C4;
    border-radius: 0;
    box-shadow: none;
    margin-bottom: 0;
}
.us-pillar-card-attention { border-top-color: #B4704D; }
.us-pillar-card-good      { border-top-color: #5B7A6E; }

.us-insight-card {
    border-top: 1.5px solid #2E261F;
    background: transparent;
    border-radius: 0;
    padding: 1rem 0 0.5rem;
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.05rem;
    line-height: 1.45;
    color: #2E261F;
}
"""


def inject() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ── Small component helpers ──────────────────────────────────────────────────

def divider(strong: bool = False) -> None:
    cls = "us-divider-strong" if strong else "us-divider"
    st.markdown(f'<hr class="{cls}">', unsafe_allow_html=True)


def meta(text: str, tone: str = "") -> str:
    """Tiny-caps meta label. tone = '', 'ink', 'clay', 'ever'."""
    cls = "us-meta"
    if tone == "ink":  cls += " us-meta-ink"
    if tone == "clay": cls += " us-meta-clay"
    if tone == "ever": cls += " us-meta-ever"
    return f'<p class="{cls}">{text}</p>'


def badge(name: str, slot: str) -> str:
    cls = "us-badge-p1" if slot == "partner1" else "us-badge-p2"
    return f'<span class="{cls}">{name}</span>'


def score_bar(value: int, slot: str) -> str:
    """Five-segment score bar. Filled segments use partner color."""
    color = COLORS["partner1"] if slot == "partner1" else COLORS["partner2"]
    segs = "".join(
        f'<span class="us-score-seg" style="background:{color if i < value else COLORS["divider"]}"></span>'
        for i in range(5)
    )
    return f'<span class="us-score-bar">{segs}</span>'


def action_bullet(text: str, index: int = 1) -> str:
    """Legacy shim: single action as numbered row (call inside a .us-action-list)."""
    num = f"{index:02d}"
    return f'<li class="us-action-item"><span class="us-action-num">{num}</span><span>{text}</span></li>'


def action_list(actions: list[str]) -> str:
    items = "".join(action_bullet(a, i + 1) for i, a in enumerate(actions))
    return f'<ul class="us-action-list">{items}</ul>'


def insight_card(text: str) -> None:
    """New styling: hairline-topped panel, no gradient, no emoji."""
    st.markdown(f'<div class="us-insight">{text}</div>', unsafe_allow_html=True)


# Kept for back-compat with any view that still calls card_open/close.
def card_open(extra_class: str = "") -> None:
    st.markdown(f'<div class="us-card {extra_class}">', unsafe_allow_html=True)


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)
