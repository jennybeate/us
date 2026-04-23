import streamlit as st
import styles
import storage
from views import welcome, context_questions, questionnaire, pillar_definition, waiting, results, checkin

st.set_page_config(
    page_title="Us",
    page_icon="♡",
    layout="centered",
    initial_sidebar_state="collapsed",
)
styles.inject()


def main():
    data = storage.load()

    p1_stage = storage.partner_stage("partner1", data)
    p2_stage = storage.partner_stage("partner2", data)

    current_name = st.session_state.get("current_partner_name")
    current_slot = storage.slot_for(current_name, data) if current_name else None

    # Both fully done → results (or check-in)
    if p1_stage == "pillars" and p2_stage == "pillars":
        if st.session_state.get("checkin_mode"):
            checkin.render(data, current_slot)
        else:
            results.render(data)
        return

    # Current user is mid-flow
    if current_name and current_slot:
        stage = storage.partner_stage(current_slot, data)
        if stage == "empty":
            context_questions.render(current_slot, current_name)
        elif stage == "context":
            questionnaire.render(current_slot, current_name)
        elif stage == "answers":
            pillar_definition.render(current_slot, current_name)
        elif stage == "pillars":
            # This partner is done; waiting for the other
            other_slot = "partner2" if current_slot == "partner1" else "partner1"
            other_stage = storage.partner_stage(other_slot, data)
            if other_stage == "pillars":
                results.render(data)
            else:
                other_name = data.get(other_slot, {}).get("name")
                waiting.render(current_name, other_name)
        return

    # No current user in session → welcome
    # Determine if partner 1 is done and we need partner 2
    if p1_stage == "pillars" and p2_stage != "pillars":
        p1_name = data["partner1"]["name"]
        welcome.render(mode="partner2", existing_name=p1_name)
    else:
        welcome.render(mode="partner1")


main()
