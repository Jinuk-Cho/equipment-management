import streamlit as st
from utils.supabase_client import get_supabase
from components.language import get_text, _normalize_language_code
from datetime import datetime, date, timedelta
import pkg_resources

# Streamlit 버전 확인 (border 매개변수 호환성 체크)
try:
    st_version = pkg_resources.get_distribution("streamlit").version
    supports_border = tuple(map(int, st_version.split('.'))) >= (1, 23, 0)
except:
    supports_border = False  # 버전 확인 실패 시 호환성 없음으로 가정

class PlanSuspensionManagementComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'ko'
        self.supabase = get_supabase()
    
    def render(self):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
        
        st.title(get_text("plan_suspension_management", lang))
        
        # 중단 중인 계획과 중단 이력 탭 생성
        tab1, tab2, tab3 = st.tabs([
            get_text("current_suspensions", lang),
            get_text("create_suspension", lang),
            get_text("suspension_history", lang)
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
            # 정지 유형 선택
            suspension_type = st.selectbox(
                get_text("suspension_type", self.lang),
                ["설비 PM", "모델 변경"]
            )
            
            # 공통 정보
            col1, col2 = st.columns(2)
            with col1:
                equipment_number = st.text_input(get_text("equipment_number", self.lang))
                building = st.selectbox(
                    get_text("building", self.lang),
                    ["A동", "B동", "C동"]
                )
            
            with col2:
                # 시작 날짜와 예상 종료 날짜
                start_date = st.date_input(get_text("start_date", self.lang), value=date.today())
                estimated_end_date = st.date_input(
                    get_text("estimated_end_date", self.lang), 
                    value=date.today() + timedelta(days=3)
                )
            
            # 담당자
            responsible_person = st.text_input(get_text("responsible_person", self.lang))
            
            # 유형별 추가 정보
            if suspension_type == "설비 PM":
                st.subheader("설비 PM 정보")
                equipment_name = st.text_input("설비명")
            else:  # 모델 변경
                st.subheader("모델 변경 정보")
                col1, col2 = st.columns(2)
                with col1:
                    model_from = st.text_input("기존 모델")
                    process_name = st.text_input("공정명")
                with col2:
                    model_to = st.text_input("신규 모델")
            
            # 세부 사유
            reason = st.text_area(get_text("reason_detail", self.lang))
            
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
                        "building": building,
                        "status": "ACTIVE"
                    }
                    
                    # 유형별 추가 데이터
                    if suspension_type == "설비 PM":
                        suspension_data["equipment_name"] = equipment_name
                    else:  # 모델 변경
                        suspension_data["model_from"] = model_from
                        suspension_data["model_to"] = model_to
                        suspension_data["process_name"] = process_name
                    
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
                    "equipment_name": "프레스 머신 1",
                    "plan_id": "설비 PM-EQ001-2023-07-15",
                    "type": "설비 PM",
                    "start_date": "2023-07-15",
                    "estimated_end_date": "2023-07-20",
                    "end_date": None,
                    "reason": "월간 예방 정비",
                    "responsible_person": "김기술",
                    "building": "A동",
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
                    "building": "B동",
                    "model_from": "모델 A",
                    "model_to": "모델 B",
                    "process_name": "조립 공정",
                    "status": "ACTIVE"
                },
                {
                    "id": 3,
                    "equipment_number": "EQ005",
                    "equipment_name": "로봇 암 2",
                    "plan_id": "설비 PM-EQ005-2023-07-12",
                    "type": "설비 PM",
                    "start_date": "2023-07-12",
                    "estimated_end_date": "2023-07-17",
                    "end_date": None,
                    "reason": "분기별 점검",
                    "responsible_person": "박엔지니어",
                    "building": "A동",
                    "status": "ACTIVE"
                },
                {
                    "id": 4,
                    "equipment_number": "EQ008",
                    "plan_id": "모델 변경-EQ008-2023-07-14",
                    "type": "모델 변경",
                    "start_date": "2023-07-14",
                    "estimated_end_date": "2023-07-21",
                    "end_date": None,
                    "reason": "신제품 출시 대응",
                    "responsible_person": "최기술",
                    "building": "C동",
                    "model_from": "모델 X",
                    "model_to": "모델 Y",
                    "process_name": "테스트 공정",
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
        
        # 건물별 필터링 옵션
        building_filter = st.selectbox(
            get_text("filter_by_building", self.lang),
            ["전체", "A동", "B동", "C동"],
            index=0
        )
        
        # 필터링 적용
        filtered_data = suspensions_data
        if suspension_type != "전체":
            filtered_data = [item for item in filtered_data if item.get("type") == suspension_type]
        
        if building_filter != "전체":
            filtered_data = [item for item in filtered_data if item.get("building") == building_filter]
            
        if not filtered_data:
            st.info(get_text("no_suspensions_of_type", self.lang))
            return
        
        # 바둑판 배열로 표시
        if suspension_type == "설비 PM" or suspension_type == "전체":
            self._display_pm_suspensions(filtered_data)
        
        if suspension_type == "모델 변경" or suspension_type == "전체":
            self._display_model_change_suspensions(filtered_data)
    
    def _display_pm_suspensions(self, data):
        """설비 PM 중인 장비를 바둑판 배열로 표시"""
        pm_data = [item for item in data if item.get("type") == "설비 PM"]
        if not pm_data:
            return
            
        st.subheader("설비 PM 현황")
        today = date.today()
        
        # 한 행에 3개씩 표시
        cols_per_row = 3
        
        # 건물별로 그룹화
        buildings = {}
        for item in pm_data:
            building = item.get("building", "기타")
            if building not in buildings:
                buildings[building] = []
            buildings[building].append(item)
        
        # 건물별로 표시
        for building, items in buildings.items():
            st.markdown(f"### {building}")
            
            # 행 개수 계산
            rows_needed = (len(items) + cols_per_row - 1) // cols_per_row
            
            for row in range(rows_needed):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    item_idx = row * cols_per_row + col_idx
                    if item_idx < len(items):
                        item = items[item_idx]
                        with cols[col_idx]:
                            # 버전 호환성을 고려한 컨테이너 생성
                            if supports_border:
                                container = st.container(border=True)
                            else:
                                container = st.container()
                                
                            with container:
                                st.markdown(f"**설비번호:** {item.get('equipment_number', 'N/A')}")
                                st.markdown(f"**설비명:** {item.get('equipment_name', 'N/A')}")
                                st.markdown(f"**시작일:** {item.get('start_date', 'N/A')}")
                                st.markdown(f"**예상종료일:** {item.get('estimated_end_date', 'N/A')}")
                                st.markdown(f"**담당자:** {item.get('responsible_person', 'N/A')}")
                                
                                # 계획 재개 버튼
                                if st.button(get_text('resume_plan', self.lang), key=f"resume_pm_{item.get('id', 0)}"):
                                    try:
                                        # 계획 재개 처리
                                        update_data = {'end_date': today.isoformat(), 'status': 'COMPLETED'}
                                        # 실제 환경에서는 다음과 같이 업데이트
                                        # result = self.supabase.table('plan_suspensions').update(update_data).eq('id', item['id']).execute()
                                        
                                        # 현재는 성공 메시지만 표시
                                        st.success(get_text('plan_resumed', self.lang))
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"{get_text('database_error', self.lang)}: {str(e)}")
    
    def _display_model_change_suspensions(self, data):
        """모델 변경 중인 장비를 바둑판 배열로 표시"""
        model_data = [item for item in data if item.get("type") == "모델 변경"]
        if not model_data:
            return
            
        st.subheader("모델 변경 현황")
        today = date.today()
        
        # 한 행에 2개씩 표시 (정보가 많아서 2개로 줄임)
        cols_per_row = 2
        
        # 건물별로 그룹화
        buildings = {}
        for item in model_data:
            building = item.get("building", "기타")
            if building not in buildings:
                buildings[building] = []
            buildings[building].append(item)
        
        # 건물별로 표시
        for building, items in buildings.items():
            st.markdown(f"### {building}")
            
            # 행 개수 계산
            rows_needed = (len(items) + cols_per_row - 1) // cols_per_row
            
            for row in range(rows_needed):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    item_idx = row * cols_per_row + col_idx
                    if item_idx < len(items):
                        item = items[item_idx]
                        with cols[col_idx]:
                            # 버전 호환성을 고려한 컨테이너 생성
                            if supports_border:
                                container = st.container(border=True)
                            else:
                                container = st.container()
                                
                            with container:
                                st.markdown(f"**설비번호:** {item.get('equipment_number', 'N/A')}")
                                st.markdown(f"**공정명:** {item.get('process_name', 'N/A')}")
                                st.markdown(f"**변경 사항:** {item.get('model_from', 'N/A')} → {item.get('model_to', 'N/A')}")
                                st.markdown(f"**시작일:** {item.get('start_date', 'N/A')}")
                                st.markdown(f"**예상종료일:** {item.get('estimated_end_date', 'N/A')}")
                                st.markdown(f"**담당자:** {item.get('responsible_person', 'N/A')}")
                                
                                # 계획 재개 버튼
                                if st.button(get_text('resume_plan', self.lang), key=f"resume_model_{item.get('id', 0)}"):
                                    try:
                                        # 계획 재개 처리
                                        update_data = {'end_date': today.isoformat(), 'status': 'COMPLETED'}
                                        # 실제 환경에서는 다음과 같이 업데이트
                                        # result = self.supabase.table('plan_suspensions').update(update_data).eq('id', item['id']).execute()
                                        
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