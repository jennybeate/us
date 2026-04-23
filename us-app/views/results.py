import streamlit as st
import plotly.graph_objects as go
import styles
import storage
import analysis
from styles import COLORS


def _radar_chart(p1_name, p1_names, p1_scores, p2_name, p2_names, p2_scores):
    fig = go.Figure()

    # Close the loop
    p1_vals = p1_scores + [p1_scores[0]] if p1_scores else []
    p1_cats = p1_names + [p1_names[0]] if p1_names else []
    p2_vals = p2_scores + [p2_scores[0]] if p2_scores else []
    p2_cats = p2_names + [p2_names[0]] if p2_names else []

    fig.add_trace(go.Scatterpolar(
        r=p1_vals,
        theta=p1_cats,
        fill="toself",
        name=p1_name,
        line=dict(color=COLORS["partner1"], width=2),
        fillcolor="rgba(201,125,110,0.15)",
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_vals,
        theta=p2_cats,
        fill="toself",
        name=p2_name,
        line=dict(color=COLORS["partner2"], width=2),
        fillcolor="rgba(126,155,138,0.15)",
        marker=dict(size=6),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=10, color="#8C6E5D"), gridcolor="#EDD9CC"),
            angularaxis=dict(tickfont=dict(size=11, family="Inter", color="#3D2B1F"), gridcolor="#EDD9CC"),
            bgcolor="#FDF6F0",
        ),
        showlegend=True,
        legend=dict(font=dict(family="Inter", size=12, color="#3D2B1F"), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="#FDF6F0",
        plot_bgcolor="#FDF6F0",
        margin=dict(l=60, r=60, t=30, b=30),
        height=380,
    )
    return fig


def _score_indicator(value: int) -> str:
    state = analysis.score_state(value)
    label = analysis.score_label(value)
    filled = "●" * value
    empty = "○" * (5 - value)
    if state == "low":
        color = COLORS["amber"]
        tag = "⚠ Needs attention"
    elif state == "high":
        color = COLORS["green"]
        tag = "✓ Feeling good"
    else:
        color = COLORS["muted"]
        tag = ""
    dots = f'<span style="color:{color};letter-spacing:2px">{filled}</span><span style="color:#EDD9CC;letter-spacing:2px">{empty}</span>'
    tag_html = f' <span style="font-size:0.75rem;color:{color};font-weight:600">{tag}</span>' if tag else ""
    return f'{dots}{tag_html} <span style="font-size:0.8rem;color:#8C6E5D">({label})</span>'


def _pillar_section(partner: dict, slot: str, other_name: str):
    name = partner["name"]
    pillars = partner.get("pillars", [])
    scores_dict = partner.get("scores", {})
    badge = styles.badge(name, slot)

    for pillar in pillars:
        pid = pillar["id"]
        pname = pillar["name"]
        score_val = scores_dict.get(pid, {}).get("value", 3)
        state = analysis.score_state(score_val)

        card_class = "us-pillar-card-attention" if state == "low" else ("us-pillar-card-good" if state == "high" else "us-pillar-card")

        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

        st.markdown(
            f"<div style='margin-bottom:0.4rem'>{badge} "
            f"<span style='font-family:Playfair Display,serif;font-size:1.1rem;font-weight:600;margin-left:0.5rem'>{pname}</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='margin-bottom:0.8rem'>{_score_indicator(score_val)}</div>",
            unsafe_allow_html=True,
        )

        # What their partner can do
        st.markdown(
            f"<p style='font-size:0.8rem;font-weight:600;color:#B09080;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.4rem'>"
            f"What {other_name} can do</p>",
            unsafe_allow_html=True,
        )

        examples = pillar.get("examples", [])
        if examples:
            # Display user-provided examples
            actions_html = "".join(styles.action_bullet(ex) for ex in examples if ex)
            st.markdown(actions_html, unsafe_allow_html=True)
        else:
            # Fall back to template actions if examples are not present (old data)
            actions = analysis.get_actions(pname, name, count=6)
            actions_html = "".join(styles.action_bullet(a) for a in actions)
            st.markdown(actions_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.8rem'></div>", unsafe_allow_html=True)


def render(data: dict):
    p1 = data.get("partner1", {})
    p2 = data.get("partner2", {})
    n1 = p1.get("name", "Partner 1")
    n2 = p2.get("name", "Partner 2")

    # Title
    st.markdown(
        f"<h1 style='text-align:center;font-style:italic;font-size:2.6rem;margin-bottom:0.2rem'>{n1} & {n2}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:1rem;margin-bottom:0.3rem'>Your relationship pillars</p>",
        unsafe_allow_html=True,
    )

    styles.divider()

    # Insights
    insights = analysis.generate_insights(p1, p2)
    if insights:
        st.markdown("#### A few things we noticed")
        for ins in insights:
            styles.insight_card(ins)
        st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # Radar chart
    p1_names, p1_scores, p2_names, p2_scores = analysis.radar_data(p1, p2)
    if p1_scores and p2_scores:
        st.markdown("#### How you're feeling right now")
        fig = _radar_chart(n1, p1_names, p1_scores, n2, p2_names, p2_scores)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    styles.divider()

    # Pillars — two columns
    st.markdown("#### What each of you needs")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        _pillar_section(p1, "partner1", n2)
    with col2:
        _pillar_section(p2, "partner2", n1)

    styles.divider()

    # Check-in CTA
    col_ci, col_r = st.columns([3, 1])
    with col_ci:
        if st.button("♡ How are we doing? Update our scores", use_container_width=True):
            st.session_state["checkin_mode"] = True
            st.rerun()

    with col_r:
        if st.button("Start over", key="reset_btn", use_container_width=True):
            storage.reset()
            st.session_state.clear()
            st.rerun()

    st.markdown(
        "<p style='text-align:center;color:#B09080;font-size:0.8rem;margin-top:2rem'>"
        "This is a living document. Come back to it. Update your scores. Grow together."
        "</p>",
        unsafe_allow_html=True,
    )
