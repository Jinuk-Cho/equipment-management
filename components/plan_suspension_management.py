import streamlit as st
from datetime import datetime, date
from components.language import get_text
from services.plan_service import PlanService

class PlanSuspensionManagementComponent:
    def __init__(self):
        self.plan_service = PlanService()

    def render(self):
        st.title(get_text("plan_suspension", st.session_state.language))
        
        tab1, tab2 = st.tabs([
            get_text("current_suspensions", st.session_state.language),
            get_text("suspension_history", st.session_state.language)
        ])
        
        with tab1:
            self.render_current_suspensions()
        
        with tab2:
            self.render_suspension_history()
    
    def render_current_suspensions(self):
        suspended_plans = self.plan_service.get_suspended_plans()
        
        if not suspended_plans:
            st.info(get_text("no_suspended_plans", st.session_state.language))
            return
        
        for plan in suspended_plans:
            with st.container():
                col1, col2, col3 = st.columns([2,2,1])
                
                with col1:
                    st.write(f"**{plan['plan_code']}**")
                    st.write(f"{get_text('equipment', st.session_state.language)}: {plan['equipment_number']}")
                
                with col2:
                    st.write(f"{get_text('suspension_period', st.session_state.language)}: "
                            f"{plan['start_date']} ~ {plan['end_date']}")
                    st.write(f"{get_text('suspension_reason', st.session_state.language)}: {plan['reason']}")
                
                with col3:
                    if st.button(get_text("resume_plan", st.session_state.language),
                               key=f"resume_{plan['plan_code']}", type="primary"):
                        if self.plan_service.resume_plan(plan['plan_code']):
                            st.success(get_text("plan_resumed", st.session_state.language))
                            st.rerun()
                
                st.divider()
    
    def render_suspension_history(self):
        history = self.plan_service.get_suspension_history()
        
        if not history:
            st.info(get_text("no_suspension_history", st.session_state.language))
            return
        
        for record in history:
            with st.expander(f"{record['plan_code']} ({record['start_date']} ~ {record['end_date']})"):
                st.write(f"{get_text('equipment', st.session_state.language)}: {record['equipment_number']}")
                st.write(f"{get_text('suspension_reason', st.session_state.language)}: {record['reason']}")
                st.write(f"{get_text('status', st.session_state.language)}: "
                        f"{get_text('completed' if record['end_date'] < date.today() else 'in_progress', st.session_state.language)}") 