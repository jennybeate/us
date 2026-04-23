import streamlit as st
import storage
import styles
from config import CONTEXT_QUESTIONS


def render(slot: str, name: str):
    q_index = st.session_state.get("cq_index", 0)
    answers = st.session_state.get("cq_answers", {})

    total = len(CONTEXT_QUESTIONS)
    q = CONTEXT_QUESTIONS[q_index]

    # Header
    st.markdown(
        f"<h2 style='text-align:center;font-style:italic;margin-bottom:0.2rem'>Getting to know you, {name}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:0.9rem;margin-bottom:1.5rem'>"
        f"A few quick questions to set the scene &nbsp;·&nbsp; {q_index + 1} of {total}"
        "</p>",
        unsafe_allow_html=True,
    )
    st.progress((q_index) / total)
    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # Framework label
    st.markdown(
        f"<p style='color:#B09080;font-size:0.75rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.3rem'>"
        f"{q['framework']}</p>",
        unsafe_allow_html=True,
    )

    # Question
    st.markdown(f"### {q['label']}")
    if q.get("hint"):
        st.markdown(
            f"<p style='color:#8C6E5D;font-size:0.85rem;margin-top:-0.8rem;margin-bottom:1rem'>{q['hint']}</p>",
            unsafe_allow_html=True,
        )

    # Input widget
    answer_key = f"cq_{q['id']}"
    current_val = answers.get(q["id"])

    if q["type"] == "slider":
        col_l, col_s, col_r = st.columns([2, 4, 2])
        with col_l:
            st.markdown(
                f"<p style='color:#8C6E5D;font-size:0.8rem;text-align:right;padding-top:0.5rem'>{q['min_label']}</p>",
                unsafe_allow_html=True,
            )
        with col_s:
            val = st.slider(
                label="",
                min_value=q["min"],
                max_value=q["max"],
                value=current_val if current_val is not None else 3,
                key=answer_key,
                label_visibility="collapsed",
            )
        with col_r:
            st.markdown(
                f"<p style='color:#8C6E5D;font-size:0.8rem;padding-top:0.5rem'>{q['max_label']}</p>",
                unsafe_allow_html=True,
            )
        answers[q["id"]] = val

    elif q["type"] == "choice":
        # st.radio returns the selected option
        default_idx = 0
        if current_val in q["options"]:
            default_idx = q["options"].index(current_val)
        val = st.radio(
            label="",
            options=q["options"],
            index=default_idx,
            key=answer_key,
            label_visibility="collapsed",
        )
        answers[q["id"]] = val

    elif q["type"] == "multiselect":
        default = current_val if isinstance(current_val, list) else []
        val = st.multiselect(
            label="",
            options=q["options"],
            default=default,
            max_selections=q.get("max_select"),
            key=answer_key,
            label_visibility="collapsed",
        )
        answers[q["id"]] = val

    st.session_state["cq_answers"] = answers

    styles.divider()

    # Navigation
    col_back, col_fwd = st.columns([1, 1])
    with col_back:
        if q_index > 0:
            if st.button("← Back", key="cq_back", use_container_width=True):
                st.session_state["cq_index"] = q_index - 1
                st.rerun()

    with col_fwd:
        is_last = q_index == total - 1
        btn_label = "Continue to reflection →" if is_last else "Next →"

        if st.button(btn_label, key="cq_next", use_container_width=True):
            # Validate
            current_answer = answers.get(q["id"])
            if q["type"] == "multiselect" and (not current_answer or len(current_answer) == 0):
                st.warning("Please select at least one option.")
                return

            if is_last:
                storage.add_context(slot, name, answers)
                st.session_state.pop("cq_index", None)
                st.session_state.pop("cq_answers", None)
                # Clear widget state
                for k in list(st.session_state.keys()):
                    if k.startswith("cq_"):
                        del st.session_state[k]
                st.rerun()
            else:
                st.session_state["cq_index"] = q_index + 1
                st.rerun()
