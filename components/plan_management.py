import streamlit as st
from components.language import get_text
from utils.supabase_client import fetch_data, insert_data, update_data, delete_data

class PlanManagementComponent:
    def __init__(self):
        pass

    def render(self):
        st.title(get_text("plan_management", st.session_state.language))
        
        tab1, tab2 = st.tabs([
            get_text("current_plans", st.session_state.language),
            get_text("create_plan", st.session_state.language)
        ])
        
        with tab1:
            self.show_plans()
        
        with tab2:
            self.create_plan()

    def show_plans(self):
        plans = fetch_data('maintenance_plans')
        if plans:
            for plan in plans:
                with st.expander(f"{plan['plan_code']} - {plan['equipment_number']}"):
                    st.write(f"상태: {plan['status']}")
                    st.write(f"시작일: {plan['start_date']}")
                    st.write(f"종료일: {plan['end_date']}")

    def create_plan(self):
        with st.form("create_plan_form"):
            equipment_number = st.text_input(get_text("equipment_number", st.session_state.language))
            start_date = st.date_input(get_text("start_date", st.session_state.language))
            end_date = st.date_input(get_text("end_date", st.session_state.language))
            
            if st.form_submit_button(get_text("create", st.session_state.language)):
                plan_data = {
                    "equipment_number": equipment_number,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "status": "SCHEDULED"
                }
                if insert_data('maintenance_plans', plan_data):
                    st.success(get_text("plan_created", st.session_state.language)) 