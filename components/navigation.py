import streamlit as st
from components.language import _normalize_language_code, get_text

class Navigation:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'ko'
    
    def render(self):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
            
        st.sidebar.title(get_text("menu", lang))
        
        menu = st.sidebar.radio(
            get_text("select_menu", lang),
            [
                get_text("dashboard", lang),
                get_text("equipment_management", lang),
                get_text("plan_management", lang),
                get_text("plan_suspension", lang),
                get_text("reports", lang),
                get_text("settings", lang)
            ]
        )
        
        return menu 