import streamlit as st
import storage
import styles


def render(mode: str = "partner1", existing_name: str | None = None):
    st.markdown(
        "<h1 style='text-align:center;font-style:italic;font-size:3.5rem;margin-bottom:0.2rem'>Us</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:1.05rem;margin-bottom:2rem'>"
        "A space to understand each other a little better."
        "</p>",
        unsafe_allow_html=True,
    )

    styles.divider()

    if mode == "partner2" and existing_name:
        st.markdown(
            f"<p style='text-align:center;color:#5A3A2B;font-size:0.95rem;margin-bottom:1.5rem'>"
            f"<strong>{existing_name}</strong> has already shared their thoughts.<br>"
            f"Now it's your turn."
            f"</p>",
            unsafe_allow_html=True,
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input(
            "What's your name?",
            placeholder="Your first name",
            key="welcome_name_input",
        )

        if mode == "partner2" and existing_name and name:
            if name.strip().lower() == existing_name.strip().lower():
                st.error(
                    f"That name is already taken. Are you {existing_name}? "
                    "Your answers are already saved — refresh the page and enter your name to continue."
                )
                return

        btn_label = "Begin" if mode == "partner1" else "Continue"
        if st.button(btn_label, use_container_width=True):
            if not name.strip():
                st.warning("Please enter your name to continue.")
                return

            data = storage.load()
            slot = storage.slot_for(name.strip(), data)
            if slot:
                # Returning user — resume their flow
                st.session_state["current_partner_name"] = name.strip()
                st.rerun()
                return

            free_slot = storage.next_free_slot(data)
            if not free_slot:
                st.error("Both partners have already completed the questionnaire. Reset to start fresh.")
                if st.button("Reset everything", key="reset_from_welcome"):
                    storage.reset()
                    st.session_state.clear()
                    st.rerun()
                return

            st.session_state["current_partner_name"] = name.strip()
            st.session_state[f"{free_slot}_name"] = name.strip()
            # Pre-register the slot so we can track stage
            data[free_slot] = {"name": name.strip()}
            storage.save(data)
            st.rerun()

    st.markdown(
        "<p style='text-align:center;color:#B09080;font-size:0.8rem;margin-top:3rem'>"
        "Your answers are private until you both finish."
        "</p>",
        unsafe_allow_html=True,
    )
