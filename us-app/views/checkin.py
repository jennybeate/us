import streamlit as st
from datetime import datetime, timezone
import storage
import styles
import analysis


def _days_ago(iso_str: str | None) -> str:
    if not iso_str:
        return "never"
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        days = delta.days
        if days == 0:
            return "today"
        if days == 1:
            return "yesterday"
        return f"{days} days ago"
    except Exception:
        return "recently"


def render(data: dict, current_slot: str | None):
    p1 = data.get("partner1", {})
    p2 = data.get("partner2", {})
    n1 = p1.get("name", "Partner 1")
    n2 = p2.get("name", "Partner 2")

    st.markdown(
        "<h2 style='text-align:center;font-style:italic;margin-bottom:0.3rem'>How are we doing?</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:0.95rem;margin-bottom:2rem'>"
        "Rate how each of your own pillars is going right now."
        "</p>",
        unsafe_allow_html=True,
    )

    # Determine who is checking in
    if current_slot:
        partner = data[current_slot]
        checkin_name = partner["name"]
    else:
        # Ask who is checking in
        checkin_name = st.radio(
            "Who is updating their scores?",
            options=[n1, n2],
            horizontal=True,
            key="checkin_who",
        )
        current_slot = "partner1" if checkin_name == n1 else "partner2"
        partner = data[current_slot]

    pillars = partner.get("pillars", [])
    scores_dict = partner.get("scores", {})

    st.markdown(
        f"<p style='color:#3D2B1F;font-size:1rem;margin-bottom:1.5rem'>"
        f"<strong>{checkin_name}</strong> — how are each of your pillars feeling right now?"
        f"</p>",
        unsafe_allow_html=True,
    )

    new_scores = {}
    for pillar in pillars:
        pid = pillar["id"]
        pname = pillar["name"]
        current_val = scores_dict.get(pid, {}).get("value", 3)
        updated_at = scores_dict.get(pid, {}).get("updated_at")

        st.markdown(
            f"<p style='font-family:Playfair Display,serif;font-size:1rem;font-weight:600;margin-bottom:0.1rem'>{pname}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p class='us-checkin-stale'>Last updated: {_days_ago(updated_at)}</p>",
            unsafe_allow_html=True,
        )

        col_l, col_s, col_r = st.columns([2, 4, 2])
        with col_l:
            st.markdown(
                "<p style='color:#8C6E5D;font-size:0.8rem;text-align:right;padding-top:0.5rem'>not feeling this</p>",
                unsafe_allow_html=True,
            )
        with col_s:
            val = st.slider(
                label="",
                min_value=1,
                max_value=5,
                value=current_val,
                key=f"ci_{pid}",
                label_visibility="collapsed",
            )
        with col_r:
            st.markdown(
                "<p style='color:#8C6E5D;font-size:0.8rem;padding-top:0.5rem'>feeling loved here</p>",
                unsafe_allow_html=True,
            )
        new_scores[pid] = val
        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    styles.divider()

    col_save, col_back = st.columns([2, 1])
    with col_save:
        if st.button("Save scores →", use_container_width=True):
            storage.update_scores(current_slot, new_scores)
            st.session_state.pop("checkin_mode", None)
            st.session_state.pop("checkin_who", None)
            for k in list(st.session_state.keys()):
                if k.startswith("ci_"):
                    del st.session_state[k]
            st.success("Scores saved.")
            st.rerun()
    with col_back:
        if st.button("← Back to pillars", use_container_width=True):
            st.session_state.pop("checkin_mode", None)
            st.rerun()
