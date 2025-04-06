import streamlit as st
import pandas as pd
import random
from components.language import _normalize_language_code, get_text
from utils.supabase_client import fetch_data, insert_data, update_data, delete_data
from datetime import datetime, date, timedelta

class PlanManagementComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'ko'

    def render(self):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
            
        st.title("계획 관리")
        
        tab1, tab2 = st.tabs([
            get_text("current_plans", lang),
            get_text("create_plan", lang)
        ])
        
        with tab1:
            self.show_plans()
        
        with tab2:
            self.create_plan()

    def show_plans(self):
        st.subheader(get_text("maintenance_plan_list", self.lang))
        
        # 필터 옵션
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                get_text("status_filter", self.lang),
                ["전체", "ACTIVE", "SUSPENDED", "COMPLETED"],
                index=0
            )
        
        with col2:
            equipment_filter = st.text_input(
                get_text("equipment_filter", self.lang),
                placeholder="설비 번호 입력"
            )
        
        with col3:
            search_btn = st.button(
                get_text("search", self.lang),
                use_container_width=True
            )
        
        # 계획 목록 가져오기
        plans = fetch_data('maintenance_plans')
        
        if not plans:
            st.info(get_text("no_plans", self.lang))
            return
        
        # 필터 적용
        if status_filter != "전체":
            plans = [p for p in plans if p['status'] == status_filter]
        
        if equipment_filter:
            plans = [p for p in plans if equipment_filter.lower() in p['equipment_number'].lower()]
        
        # 계획 목록 표시
        st.markdown("---")
        for plan in plans:
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{plan['plan_code']}**")
                    st.markdown(f"**{get_text('equipment', self.lang)}:** {plan['equipment_number']}")
                
                with col2:
                    st.markdown(f"**{get_text('period', self.lang)}:** {plan['start_date']} ~ {plan['end_date']}")
                    
                    status_color = {
                        'ACTIVE': 'green',
                        'SUSPENDED': 'orange',
                        'COMPLETED': 'blue'
                    }.get(plan['status'], 'gray')
                    
                    st.markdown(f"**{get_text('status', self.lang)}:** <span style='color:{status_color};'>{plan['status']}</span>", unsafe_allow_html=True)
                
                with col3:
                    if plan['status'] == 'ACTIVE':
                        if st.button(get_text("suspend", self.lang), key=f"suspend_{plan['id']}", type="secondary"):
                            st.session_state.selected_plan = plan
                            st.session_state.show_suspend_form = True
                    elif plan['status'] == 'SUSPENDED':
                        if st.button(get_text("resume", self.lang), key=f"resume_{plan['id']}", type="primary"):
                            # 실제로는 API 호출이 필요합니다
                            st.success(get_text("plan_resumed", self.lang))
                            st.rerun()
                
                st.markdown("---")
        
        # 정지 폼 표시
        if 'show_suspend_form' in st.session_state and st.session_state.show_suspend_form:
            self.show_suspend_form()

    def show_suspend_form(self):
        plan = st.session_state.selected_plan
        
        with st.form("suspend_plan_form"):
            st.subheader(f"{plan['plan_code']} {get_text('suspension', self.lang)}")
            
            today = date.today()
            start_date = st.date_input(
                get_text("suspension_start_date", self.lang),
                value=today
            )
            
            end_date = st.date_input(
                get_text("suspension_end_date", self.lang),
                value=today + timedelta(days=7)
            )
            
            reason = st.text_area(
                get_text("suspension_reason", self.lang),
                placeholder=get_text("enter_reason", self.lang)
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(get_text("suspend_plan", self.lang), type="primary", use_container_width=True):
                    # 실제로는 API 호출이 필요합니다
                    st.success(get_text("plan_suspended", self.lang))
                    st.session_state.show_suspend_form = False
                    st.rerun()
            
            with col2:
                if st.form_submit_button(get_text("cancel", self.lang), use_container_width=True):
                    st.session_state.show_suspend_form = False
                    st.rerun()

    def create_plan(self):
        st.subheader(get_text("create_new_plan", self.lang))
        
        with st.form("create_plan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                equipment_number = st.text_input(
                    get_text("equipment_number", self.lang),
                    placeholder="EQ001"
                )
                
                maintenance_type = st.selectbox(
                    get_text("maintenance_type", self.lang),
                    ["정기 점검", "부품 교체", "소프트웨어 업데이트", "기타"]
                )
            
            with col2:
                start_date = st.date_input(
                    get_text("start_date", self.lang),
                    value=date.today()
                )
                
                end_date = st.date_input(
                    get_text("end_date", self.lang),
                    value=date.today() + timedelta(days=30)
                )
            
            description = st.text_area(
                get_text("plan_description", self.lang),
                placeholder=get_text("enter_plan_details", self.lang)
            )
            
            # 자동 생성된 계획 코드
            today_str = datetime.today().strftime('%Y%m%d')
            plan_code = f"MP{today_str}-{equipment_number}"
            
            st.info(f"{get_text('plan_code', self.lang)}: {plan_code}")
            
            if st.form_submit_button(get_text("create_plan", self.lang), type="primary", use_container_width=True):
                if not equipment_number:
                    st.error(get_text("enter_equipment_number", self.lang))
                    return
                
                if start_date > end_date:
                    st.error(get_text("date_error", self.lang))
                    return
                
                plan_data = {
                    "plan_code": plan_code,
                    "equipment_number": equipment_number,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "description": description,
                    "maintenance_type": maintenance_type,
                    "status": "ACTIVE",
                    "created_at": datetime.now().isoformat()
                }
                
                # 실제로는 API 호출이 필요합니다
                # 지금은 성공으로 처리
                st.success(get_text("plan_created", self.lang))
                st.balloons() 