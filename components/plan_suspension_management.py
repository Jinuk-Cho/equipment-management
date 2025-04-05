import streamlit as st
from utils.supabase_client import get_supabase
from components.language import get_text
from datetime import datetime, date

class PlanSuspensionManagementComponent:
    def __init__(self, lang='ko'):
        self.lang = lang
        self.supabase = get_supabase()
    
    def render(self):
        st.title(get_text("plan_suspension_management", self.lang))
        
        # 중단 중인 계획과 중단 이력 탭 생성
        tab1, tab2, tab3 = st.tabs([
            get_text("current_suspensions", self.lang),
            get_text("create_suspension", self.lang),
            get_text("suspension_history", self.lang)
        ])
        
        # 중단 중인 계획 탭
        with tab1:
            self.render_current_suspensions()
        
        # 새 중단 계획 생성 탭
        with tab2:
            self.create_suspension()
            
        # 중단 이력 탭
        with tab3:
            self.render_suspension_history()
    
    def create_suspension(self):
        """새로운 계획 정지 등록 폼"""
        st.subheader(get_text("register_new_suspension", self.lang))
        
        with st.form("new_suspension_form"):
            # 설비 정보
            equipment_number = st.text_input(get_text("equipment_number", self.lang))
            
            # 정지 유형 선택
            suspension_type = st.selectbox(
                get_text("suspension_type", self.lang),
                ["설비 PM", "모델 변경"]
            )
            
            # 시작 날짜와 예상 종료 날짜
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(get_text("start_date", self.lang), value=date.today())
            with col2:
                estimated_end_date = st.date_input(
                    get_text("estimated_end_date", self.lang), 
                    value=date.today() + datetime.timedelta(days=3)
                )
            
            # 세부 사유
            reason = st.text_area(get_text("reason_detail", self.lang))
            
            # 담당자
            responsible_person = st.text_input(get_text("responsible_person", self.lang))
            
            # 제출 버튼
            submitted = st.form_submit_button(get_text("register", self.lang))
            
            if submitted:
                if not equipment_number:
                    st.error(get_text("enter_equipment_number", self.lang))
                    return
                
                try:
                    # 데이터 준비
                    suspension_data = {
                        "equipment_number": equipment_number,
                        "plan_id": f"{suspension_type}-{equipment_number}-{start_date}",
                        "type": suspension_type,
                        "start_date": str(start_date),
                        "estimated_end_date": str(estimated_end_date),
                        "end_date": None,  # 아직 종료되지 않음
                        "reason": reason,
                        "responsible_person": responsible_person,
                        "status": "ACTIVE"
                    }
                    
                    # 실제 환경에서는 다음과 같이 데이터베이스에 저장
                    # result = self.supabase.table('plan_suspensions').insert(suspension_data).execute()
                    
                    # 현재는 성공 메시지만 표시
                    st.success(get_text("suspension_registered", self.lang))
                    st.balloons()
                except Exception as e:
                    st.error(f"{get_text('registration_failed', self.lang)}: {str(e)}")
    
    def render_current_suspensions(self):
        # 현재 중단된 계획 정보 가져오기
        today = date.today()
        
        try:
            suspensions = self.supabase.table('plan_suspensions').select('*').is_('end_date', 'null').execute()
            suspensions_data = suspensions.data
        except Exception as e:
            st.warning(f"{get_text('database_error', self.lang)}: plan_suspensions 테이블이 존재하지 않습니다.")
            # 가상 데이터 생성
            suspensions_data = [
                {
                    "id": 1,
                    "equipment_number": "EQ001",
                    "plan_id": "설비 PM-EQ001-2023-07-15",
                    "type": "설비 PM",
                    "start_date": "2023-07-15",
                    "estimated_end_date": "2023-07-20",
                    "end_date": None,
                    "reason": "월간 예방 정비",
                    "responsible_person": "김기술",
                    "status": "ACTIVE"
                },
                {
                    "id": 2,
                    "equipment_number": "EQ003",
                    "plan_id": "모델 변경-EQ003-2023-07-10",
                    "type": "모델 변경",
                    "start_date": "2023-07-10",
                    "estimated_end_date": "2023-07-18",
                    "end_date": None,
                    "reason": "신규 모델 적용",
                    "responsible_person": "이엔지니어",
                    "status": "ACTIVE"
                }
            ]
        
        if not suspensions_data:
            st.info(get_text("no_suspended_plans", self.lang))
            return
        
        # 유형별 필터링 옵션
        suspension_type = st.selectbox(
            get_text("filter_by_type", self.lang),
            ["전체", "설비 PM", "모델 변경"],
            index=0
        )
        
        # 필터링 적용
        if suspension_type != "전체":
            filtered_data = [item for item in suspensions_data if item.get("type") == suspension_type]
        else:
            filtered_data = suspensions_data
            
        if not filtered_data:
            st.info(get_text("no_suspensions_of_type", self.lang))
            return
            
        # 중단된 계획 목록 표시
        for record in filtered_data:
            with st.expander(f"{record.get('type', '정지')} - {record.get('equipment_number', 'N/A')} ({record.get('start_date', 'N/A')})"):
                st.write(f"**{get_text('equipment_number', self.lang)}:** {record.get('equipment_number', 'N/A')}")
                st.write(f"**{get_text('suspension_type', self.lang)}:** {record.get('type', 'N/A')}")
                st.write(f"**{get_text('suspension_date', self.lang)}:** {record.get('start_date', 'N/A')}")
                st.write(f"**{get_text('estimated_end_date', self.lang)}:** {record.get('estimated_end_date', 'N/A')}")
                st.write(f"**{get_text('reason', self.lang)}:** {record.get('reason', 'N/A')}")
                st.write(f"**{get_text('responsible_person', self.lang)}:** {record.get('responsible_person', 'N/A')}")
                
                # 계획 재개 버튼
                if st.button(get_text('resume_plan', self.lang), key=f"resume_{record.get('id', 0)}"):
                    try:
                        # 계획 재개 처리
                        update_data = {'end_date': today.isoformat(), 'status': 'COMPLETED'}
                        # 실제 환경에서는 다음과 같이 업데이트
                        # result = self.supabase.table('plan_suspensions').update(update_data).eq('id', record['id']).execute()
                        
                        # 현재는 성공 메시지만 표시
                        st.success(get_text('plan_resumed', self.lang))
                        st.rerun()
                    except Exception as e:
                        st.error(f"{get_text('database_error', self.lang)}: {str(e)}")
    
    def render_suspension_history(self):
        try:
            # 중단 이력 가져오기 (종료일이 있는 경우)
            history = self.supabase.table('plan_suspensions').select('*').not_.is_('end_date', 'null').execute()
            history_data = history.data
        except Exception as e:
            st.warning(f"{get_text('database_error', self.lang)}: plan_suspensions 테이블이 존재하지 않습니다.")
            # 가상 데이터 생성
            history_data = [
                {
                    "id": 3,
                    "equipment_number": "EQ002",
                    "plan_id": "설비 PM-EQ002-2023-06-01",
                    "type": "설비 PM",
                    "start_date": "2023-06-01",
                    "estimated_end_date": "2023-06-05",
                    "end_date": "2023-06-04",
                    "reason": "분기별 예방 정비",
                    "responsible_person": "박정비",
                    "status": "COMPLETED"
                },
                {
                    "id": 4,
                    "equipment_number": "EQ005",
                    "plan_id": "모델 변경-EQ005-2023-05-20",
                    "type": "모델 변경",
                    "start_date": "2023-05-20",
                    "estimated_end_date": "2023-05-25",
                    "end_date": "2023-05-27",
                    "reason": "모델 A에서 모델 B로 전환",
                    "responsible_person": "최엔지니어",
                    "status": "COMPLETED"
                }
            ]
        
        if not history_data:
            st.info(get_text("no_suspension_history", self.lang))
            return
        
        # 유형별 필터링 옵션
        history_type = st.selectbox(
            get_text("filter_history_by_type", self.lang),
            ["전체", "설비 PM", "모델 변경"],
            index=0,
            key="history_type_filter"
        )
        
        # 필터링 적용
        if history_type != "전체":
            filtered_history = [item for item in history_data if item.get("type") == history_type]
        else:
            filtered_history = history_data
            
        if not filtered_history:
            st.info(get_text("no_history_of_type", self.lang))
            return
            
        # 현재 날짜 가져오기
        today = date.today()
        
        # 중단 이력 표시
        for record in filtered_history:
            # 완료 여부 확인
            status = get_text("completed", self.lang)
            
            with st.expander(f"{record.get('type', '정지')} - {record.get('equipment_number', 'N/A')} ({record.get('start_date', 'N/A')} ~ {record.get('end_date', 'N/A')})"):
                st.write(f"**{get_text('equipment_number', self.lang)}:** {record.get('equipment_number', 'N/A')}")
                st.write(f"**{get_text('suspension_type', self.lang)}:** {record.get('type', 'N/A')}")
                st.write(f"**{get_text('suspension_date', self.lang)}:** {record.get('start_date', 'N/A')}")
                st.write(f"**{get_text('resume_date', self.lang)}:** {record.get('end_date', 'N/A')}")
                st.write(f"**{get_text('reason', self.lang)}:** {record.get('reason', 'N/A')}")
                st.write(f"**{get_text('responsible_person', self.lang)}:** {record.get('responsible_person', 'N/A')}")
                st.write(f"**{get_text('status', self.lang)}:** {status}") 