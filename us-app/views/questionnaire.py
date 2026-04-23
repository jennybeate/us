import streamlit as st
import storage
import styles
from config import QUESTIONS


def render(slot: str, name: str):
    q_index = st.session_state.get("q_index", 0)
    answers = st.session_state.get("q_answers", {})

    total = len(QUESTIONS)
    q = QUESTIONS[q_index]

    # Header
    st.markdown(
        f"<h2 style='text-align:center;font-style:italic;margin-bottom:0.2rem'>In your own words, {name}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:0.9rem;margin-bottom:1.5rem'>"
        f"Take your time with each answer &nbsp;·&nbsp; {q_index + 1} of {total}"
        "</p>",
        unsafe_allow_html=True,
    )
    st.progress((q_index) / total)
    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # Theme label
    st.markdown(
        f"<p style='color:#B09080;font-size:0.75rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.3rem'>"
        f"{q['theme']}</p>",
        unsafe_allow_html=True,
    )

    # Question
    st.markdown(f"### {q['label']}")
    st.markdown(
        f"<p style='color:#8C6E5D;font-size:0.85rem;margin-top:-0.8rem;margin-bottom:1rem'>{q['hint']}</p>",
        unsafe_allow_html=True,
    )

    current_val = answers.get(q["id"], "")
    val = st.text_area(
        label="",
        value=current_val,
        placeholder=q["placeholder"],
        height=140,
        key=f"q_{q['id']}",
        label_visibility="collapsed",
    )
    answers[q["id"]] = val
    st.session_state["q_answers"] = answers

    styles.divider()

    col_back, col_fwd = st.columns([1, 1])
    with col_back:
        if q_index > 0:
            if st.button("← Back", key="q_back", use_container_width=True):
                st.session_state["q_index"] = q_index - 1
                st.rerun()

    with col_fwd:
        is_last = q_index == total - 1
        btn_label = "Continue to pillars →" if is_last else "Next →"

        if st.button(btn_label, key="q_next", use_container_width=True):
            if not val.strip():
                st.warning("Please write something before continuing — even a sentence is enough.")
                return

            if is_last:
                storage.add_answers(slot, name, answers)
                st.session_state.pop("q_index", None)
                st.session_state.pop("q_answers", None)
                for k in list(st.session_state.keys()):
                    if k.startswith("q_"):
                        del st.session_state[k]
                st.rerun()
            else:
                st.session_state["q_index"] = q_index + 1
                st.rerun()
