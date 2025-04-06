import streamlit as st
from datetime import datetime, date
from services.plan_service import PlanService
from components.language import _normalize_language_code, get_text

class PlanSuspensionComponent:
    def __init__(self, lang=None):
        self.plan_service = PlanService()
        self.lang = lang if lang else 'ko'

    def render(self, plan_code=None):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
            
        st.subheader("계획 정지")
        
        with st.form("plan_suspension_form"):
            start_date = st.date_input(
                "정지 시작일",
                min_value=date.today(),
                value=date.today()
            )
            
            end_date = st.date_input(
                "정지 종료일",
                min_value=start_date,
                value=start_date
            )
            
            reason = st.text_area("정지 사유")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("정지"):
                    if start_date > end_date:
                        st.error("종료일은 시작일보다 빠를 수 없습니다.")
                        return
                    
                    success = self.plan_service.suspend_plan(
                        plan_code=plan_code,
                        start_date=start_date,
                        end_date=end_date,
                        reason=reason
                    )
                    
                    if success:
                        st.success("계획이 정지되었습니다.")
                        return True
                    else:
                        st.error("계획 정지 중 오류가 발생했습니다.")
                        return False
            
            with col2:
                if st.form_submit_button("취소"):
                    return True 