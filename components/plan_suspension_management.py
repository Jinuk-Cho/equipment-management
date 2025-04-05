import streamlit as st
from utils.supabase_client import get_supabase_client
from components.language import get_text
from datetime import datetime, date

class PlanSuspensionManagementComponent:
    def __init__(self, lang='ko'):
        self.lang = lang
        self.supabase = get_supabase_client()
    
    def render(self):
        st.title(get_text("plan_suspension_management", self.lang))
        
        # 중단 중인 계획과 중단 이력 탭 생성
        tab1, tab2 = st.tabs([
            get_text("current_suspensions", self.lang),
            get_text("suspension_history", self.lang)
        ])
        
        # 중단 중인 계획 탭
        with tab1:
            self.render_current_suspensions()
        
        # 중단 이력 탭
        with tab2:
            self.render_suspension_history()
    
    def render_current_suspensions(self):
        # 현재 중단된 계획 정보 가져오기
        today = date.today()
        suspensions = self.supabase.table('plan_suspensions').select('*').is_('end_date', 'null').execute()
        
        if not suspensions.data:
            st.info(get_text("no_suspended_plans", self.lang))
            return
        
        # 중단된 계획 목록 표시
        for record in suspensions.data:
            with st.expander(f"{get_text('plan', self.lang)}: {record['plan_id']} - {record['reason']}"):
                st.write(f"{get_text('suspension_date', self.lang)}: {record['start_date']}")
                st.write(f"{get_text('reason', self.lang)}: {record['reason']}")
                
                # 계획 재개 버튼
                if st.button(get_text('resume_plan', self.lang), key=f"resume_{record['id']}"):
                    # 계획 재개 처리
                    update_data = {'end_date': today.isoformat()}
                    result = self.supabase.table('plan_suspensions').update(update_data).eq('id', record['id']).execute()
                    
                    if result.data:
                        st.success(get_text('plan_resumed', self.lang))
                        st.rerun()
                    else:
                        st.error(get_text('failed_to_resume', self.lang))
    
    def render_suspension_history(self):
        # 중단 이력 가져오기 (종료일이 있는 경우)
        history = self.supabase.table('plan_suspensions').select('*').not_.is_('end_date', 'null').execute()
        
        if not history.data:
            st.info(get_text("no_suspension_history", self.lang))
            return
        
        # 현재 날짜 가져오기
        today = date.today()
        
        # 중단 이력 표시
        for record in history.data:
            try:
                # 문자열 형태의 end_date를 datetime.date 객체로 변환
                end_date = None
                if record['end_date']:
                    try:
                        end_date = datetime.strptime(record['end_date'], "%Y-%m-%d").date()
                    except:
                        try:
                            end_date = datetime.strptime(record['end_date'], "%Y/%m/%d").date()
                        except:
                            end_date = None
                
                # 완료 여부 확인
                status = get_text("completed", self.lang)
                if end_date and end_date > today:
                    status = get_text("in_progress", self.lang)
            except Exception as e:
                # 오류가 발생하면 진행 중으로 처리
                status = get_text("in_progress", self.lang)
            
            with st.expander(f"{get_text('plan', self.lang)}: {record['plan_id']} - {status}"):
                st.write(f"{get_text('suspension_date', self.lang)}: {record['start_date']}")
                st.write(f"{get_text('resume_date', self.lang)}: {record['end_date']}")
                st.write(f"{get_text('reason', self.lang)}: {record['reason']}")
                st.write(f"{get_text('status', self.lang)}: {status}") 