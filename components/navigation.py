import streamlit as st
from components.language import get_text

class NavigationComponent:
    def __init__(self):
        pass

    def render(self):
        st.sidebar.title(get_text("menu", st.session_state.language))
        
        menu = st.sidebar.radio(
            get_text("select_menu", st.session_state.language),
            [
                get_text("dashboard", st.session_state.language),
                get_text("equipment_management", st.session_state.language),
                get_text("plan_management", st.session_state.language),
                get_text("plan_suspension", st.session_state.language),
                get_text("reports", st.session_state.language),
                get_text("settings", st.session_state.language)
            ]
        )
        
        return menu 