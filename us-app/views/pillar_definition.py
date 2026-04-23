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
        "Name up to 5 in your own words. The first 3 are required. For each pillar, give 5 concrete examples of things your partner does or could do to honour that pillar."
        "</p>",
        unsafe_allow_html=True,
    )

    pillars_raw = []
    validation_errors = []

    for i in range(5):
        required = i < 3
        label = f"Pillar {i + 1}" + (" *" if required else " (optional)")
        placeholder = PILLAR_PLACEHOLDERS[i] if i < len(PILLAR_PLACEHOLDERS) else "Something that matters to you"

        pname = st.text_input(
            label,
            placeholder=placeholder,
            key=f"pillar_name_{i}",
        )

        if pname.strip():
            st.markdown(f"<p style='font-size:0.85rem;color:#8C6E5D;margin-top:-0.5rem'>Examples of what {name} does or could do to make you feel <strong>{pname.strip()}</strong>:</p>", unsafe_allow_html=True)
            examples = []
            for j in range(5):
                ex = st.text_input(
                    f"Example {j + 1}",
                    placeholder=f"e.g., They listen without trying to fix things...",
                    key=f"pillar_ex_{i}_{j}",
                    label_visibility="collapsed",
                )
                examples.append(ex.strip())

            # Validate all 5 examples are filled
            if any(ex == "" for ex in examples):
                validation_errors.append(f"Pillar '{pname.strip()}' needs all 5 examples filled.")
            else:
                pillars_raw.append({
                    "id": f"p{i+1}",
                    "name": pname.strip(),
                    "examples": examples,
                })

    styles.divider()

    if st.button("Save my pillars →", use_container_width=False):
        # Validate at least 3
        if len(pillars_raw) < 3:
            st.warning("Please name and complete at least 3 pillars before continuing.")
            return

        # Check for validation errors
        if validation_errors:
            for error in validation_errors:
                st.error(error)
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
