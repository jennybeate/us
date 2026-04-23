"""
Drop-in replacement for results.py.

Changes vs. original:
- Header uses asymmetric display type (Partner1 / and / Partner2), not centered italic.
- Radar is understated: hairline grid, small clay / evergreen polygons, dashed
  line on partner 2 so colorblind users can still distinguish the two.
- Pillar sections are ROWS (hairline top rule), not drop-shadowed cards.
  Each row shows: partner label, pillar name (Fraunces), score bar + '/5',
  and a numbered list of actions typeset in Fraunces to read as the partner's
  voice rather than template copy.
- Insights use hairline-topped panels, Fraunces display type, no gradient, no 💡.
- CTA buttons are solid-ink (no gradient); 'Start over' is a ghost button.
- Still depends on: storage, analysis, styles. No new dependencies.
"""

import streamlit as st
import plotly.graph_objects as go
import styles
import storage
import analysis
from styles import COLORS


# ── Radar chart ──────────────────────────────────────────────────────────────

def _radar_chart(p1_name, p1_names, p1_scores, p2_name, p2_names, p2_scores):
    fig = go.Figure()

    p1_vals = p1_scores + [p1_scores[0]] if p1_scores else []
    p1_cats = p1_names + [p1_names[0]] if p1_names else []
    p2_vals = p2_scores + [p2_scores[0]] if p2_scores else []
    p2_cats = p2_names + [p2_names[0]] if p2_names else []

    fig.add_trace(go.Scatterpolar(
        r=p1_vals,
        theta=p1_cats,
        fill="toself",
        name=p1_name,
        line=dict(color=COLORS["partner1"], width=1.4),
        fillcolor="rgba(180,112,77,0.12)",   # clay @ 12%
        marker=dict(size=4, color=COLORS["partner1"]),
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_vals,
        theta=p2_cats,
        fill="toself",
        name=p2_name,
        line=dict(color=COLORS["partner2"], width=1.4, dash="dash"),
        fillcolor="rgba(91,122,110,0.10)",   # evergreen @ 10%
        marker=dict(size=4, color=COLORS["partner2"]),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 5],
                tickfont=dict(size=9, color="#8B7F74"),
                gridcolor="#DBD2C4",
                linecolor="#DBD2C4",
                showline=False,
            ),
            angularaxis=dict(
                tickfont=dict(size=10, family="JetBrains Mono", color="#2E261F"),
                gridcolor="#DBD2C4",
                linecolor="#DBD2C4",
            ),
            bgcolor="#F7F3EC",
        ),
        showlegend=True,
        legend=dict(
            font=dict(family="JetBrains Mono", size=10, color="#2E261F"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=-0.12,
            xanchor="center", x=0.5,
        ),
        paper_bgcolor="#F7F3EC",
        plot_bgcolor="#F7F3EC",
        margin=dict(l=60, r=60, t=20, b=40),
        height=420,
    )
    return fig


# ── Pillar row ───────────────────────────────────────────────────────────────

def _pillar_row(partner: dict, slot: str, other_name: str, is_first: bool, index: int):
    name = partner["name"]
    pillars = partner.get("pillars", [])
    scores_dict = partner.get("scores", {})

    if not pillars:
        return index

    partner_color_class = "us-meta-clay" if slot == "partner1" else "us-meta-ever"

    for pillar in pillars:
        pid = pillar["id"]
        pname = pillar["name"]
        pdesc = pillar.get("description", "")
        score_val = scores_dict.get(pid, {}).get("value", 3)
        state = analysis.score_state(score_val)

        state_tag = ""
        if state == "low":
            state_tag = '<span class="us-tag-attn">• Needs attention</span>'
        elif state == "high":
            state_tag = '<span class="us-tag-good">• Feeling good</span>'

        row_cls = "us-pillar-row" + (" us-pillar-row-first" if is_first else "")
        is_first = False  # only the first row in the section gets the heavy rule

        # Meta row: "01 · Maya · Needs attention"
        num = f"{index:02d}"
        meta_line = (
            f'<p class="us-meta {partner_color_class}" style="margin-bottom:0.35rem">'
            f'{num} &nbsp;·&nbsp; {name}'
            f'{"&nbsp;&nbsp;" + state_tag if state_tag else ""}'
            f'</p>'
        )

        # Left column: pillar name + score bar. Right: numbered list of actions.
        st.markdown(f'<div class="{row_cls}">', unsafe_allow_html=True)
        st.markdown(meta_line, unsafe_allow_html=True)

        left, right = st.columns([1, 1.2], gap="large")
        with left:
            st.markdown(
                f'<div class="us-display" style="font-size:1.5rem;margin:0 0 0.5rem">{pname}</div>',
                unsafe_allow_html=True,
            )
            if pdesc:
                st.markdown(
                    f'<p class="us-quiet" style="font-size:0.95rem;margin:0 0 0.6rem">{pdesc}</p>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div style="display:flex;gap:0.6rem;align-items:center;margin-top:0.25rem">'
                f'{styles.score_bar(score_val, slot)}'
                f'<span class="us-meta">{score_val}/5</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(
                styles.meta(f"What {other_name} can do — in {name}'s words"),
                unsafe_allow_html=True,
            )
            actions = analysis.get_actions(pname, name, count=5)
            st.markdown(styles.action_list(actions), unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        index += 1

    return index


# ── Main render ──────────────────────────────────────────────────────────────

def render(data: dict):
    p1 = data.get("partner1", {})
    p2 = data.get("partner2", {})
    n1 = p1.get("name", "Partner 1")
    n2 = p2.get("name", "Partner 2")

    # ── Header ──
    header_left, header_right = st.columns([1, 1], gap="large")
    with header_left:
        st.markdown(styles.meta("Shared results"), unsafe_allow_html=True)
        st.markdown(
            f'<h1 class="us-display" style="font-size:3.6rem;margin:0.4rem 0 0">'
            f'<span style="color:{COLORS["partner1"]}">{n1}</span><br>'
            f'<span style="color:{COLORS["muted"]};font-weight:300">and</span><br>'
            f'<span style="color:{COLORS["partner2"]}">{n2}</span>'
            f'</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="margin-top:1.25rem;font-size:1rem;line-height:1.65;color:#5A4F46;max-width:26rem">'
            "You&rsquo;ve each named the things that matter most. "
            "Here&rsquo;s where you meet &mdash; and where you can meet each other better."
            "</p>",
            unsafe_allow_html=True,
        )

    with header_right:
        p1_names, p1_scores, p2_names, p2_scores = analysis.radar_data(p1, p2)
        if p1_scores and p2_scores:
            fig = _radar_chart(n1, p1_names, p1_scores, n2, p2_names, p2_scores)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

    # ── Insights ──
    insights = analysis.generate_insights(p1, p2)
    if insights:
        st.markdown(styles.meta("What we noticed"), unsafe_allow_html=True)
        ic1, ic2 = st.columns(2, gap="large")
        buckets = [ic1, ic2]
        for i, ins in enumerate(insights[:4]):
            with buckets[i % 2]:
                styles.insight_card(ins)

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

    # ── Pillar sections ──
    st.markdown(
        styles.meta(f"What each of you needs — in your own words"),
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    idx = 1
    idx = _pillar_row(p1, "partner1", n2, is_first=True, index=idx)
    idx = _pillar_row(p2, "partner2", n1, is_first=False, index=idx)

    # ── Footer / CTAs ──
    styles.divider(strong=True)

    foot_left, foot_right = st.columns([2, 1], gap="large")
    with foot_left:
        st.markdown(
            '<div class="us-display" style="font-size:1.4rem;margin:0">'
            "This is a living document."
            "</div>"
            '<p class="us-meta" style="margin-top:0.3rem">'
            "Come back &nbsp;·&nbsp; Update scores &nbsp;·&nbsp; Grow together"
            "</p>",
            unsafe_allow_html=True,
        )
    with foot_right:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Start over", key="reset_btn", type="secondary", use_container_width=True):
                storage.reset()
                st.session_state.clear()
                st.rerun()
        with c2:
            if st.button("How are we doing? →", key="checkin_btn", use_container_width=True):
                st.session_state["checkin_mode"] = True
                st.rerun()
