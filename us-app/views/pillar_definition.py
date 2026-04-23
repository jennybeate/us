import streamlit as st
import storage
import styles
from config import PILLAR_PLACEHOLDERS


def render(slot: str, name: str):
    st.markdown(
        f"<h2 style='text-align:center;font-style:italic;margin-bottom:0.2rem'>Your pillars, {name}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:0.95rem;margin-bottom:0.5rem'>"
        "Based on your answers, what are the things that matter most to you in a relationship?"
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#B09080;font-size:0.85rem;margin-bottom:2rem'>"
        "Name up to 5 in your own words. The first 3 are required."
        "</p>",
        unsafe_allow_html=True,
    )

    pillars_raw = []
    for i in range(5):
        required = i < 3
        label = f"Pillar {i + 1}" + (" *" if required else " (optional)")
        placeholder = PILLAR_PLACEHOLDERS[i] if i < len(PILLAR_PLACEHOLDERS) else "Something that matters to you"

        col_name, col_desc = st.columns([2, 3])
        with col_name:
            pname = st.text_input(
                label,
                placeholder=placeholder,
                key=f"pillar_name_{i}",
            )
        with col_desc:
            pdesc = st.text_input(
                "Description (optional)",
                placeholder="A little more detail...",
                key=f"pillar_desc_{i}",
                label_visibility="visible" if i == 0 else "collapsed",
            )
        if pname.strip():
            pillars_raw.append({"id": f"p{i+1}", "name": pname.strip(), "description": pdesc.strip()})

    styles.divider()

    if st.button("Save my pillars →", use_container_width=False):
        # Validate at least 3
        if len(pillars_raw) < 3:
            st.warning("Please name at least 3 pillars before continuing.")
            return

        storage.add_pillars(slot, pillars_raw)

        # Initialise scores to 3 (middle)
        scores = {p["id"]: 3 for p in pillars_raw}
        storage.update_scores(slot, scores)

        # Clean up widget state
        for k in list(st.session_state.keys()):
            if k.startswith("pillar_"):
                del st.session_state[k]
        st.rerun()
