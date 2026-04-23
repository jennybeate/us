import streamlit as st
import styles


def render(current_name: str, other_name: str | None):
    st.markdown(
        f"<h2 style='text-align:center;font-style:italic;margin-bottom:0.5rem'>"
        f"Thank you, {current_name}."
        f"</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#8C6E5D;font-size:1rem;margin-bottom:2rem'>"
        "Your thoughts are safe here."
        "</p>",
        unsafe_allow_html=True,
    )

    styles.divider()

    if other_name:
        msg = f"Now hand the computer to <strong>{other_name}</strong> and let them share their turn."
    else:
        msg = "Now hand the computer to your partner and let them share their turn."

    st.markdown(
        f"<p style='text-align:center;font-size:1.05rem;color:#3D2B1F;margin-bottom:1rem'>{msg}</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#B09080;font-size:0.9rem;margin-bottom:2.5rem'>"
        "Once you've both shared, you'll see your relationship pillars together."
        "</p>",
        unsafe_allow_html=True,
    )

    # Large decorative heart
    st.markdown(
        "<p style='text-align:center;font-size:3rem;margin:1.5rem 0'>♡</p>",
        unsafe_allow_html=True,
    )

    styles.divider()

    # Allow switching partners without knowing the name
    st.markdown(
        "<p style='text-align:center;color:#B09080;font-size:0.8rem;margin-top:1rem'>"
        "When your partner is ready, they can enter their name on the next screen."
        "</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Hand over →", use_container_width=True):
            # Clear current session so partner 2 sees welcome
            st.session_state.pop("current_partner_name", None)
            st.rerun()
