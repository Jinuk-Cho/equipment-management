import streamlit as st
from components.language import _normalize_language_code, get_text
from utils.supabase_client import get_supabase, fetch_data, update_data, delete_data, insert_data

class AdminComponent:
    def __init__(self, lang=None):
        self.supabase = get_supabase()
        self.lang = lang if lang else 'ko'

    def render(self):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
            
        st.title(get_text("admin_settings", lang))
        
        # 탭 생성
        tabs = st.tabs([
            get_text("user_management", lang),
            get_text("equipment_management", lang),
            get_text("error_codes", lang)
        ])
        
        with tabs[0]:
            self.render_user_management()
        
        with tabs[1]:
            self.render_equipment_management()
            
        with tabs[2]:
            self.render_error_codes()

    def render_user_management(self):
        # 사용자 관리 UI 구현
        pass

    def render_equipment_management(self):
        # 설비 관리 UI 구현
        pass

    def render_error_codes(self):
        # 오류 코드 관리 UI 구현
        pass 