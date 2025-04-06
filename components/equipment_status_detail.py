import streamlit as st
import pandas as pd
from components.language import get_text

class EquipmentStatusDetailComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'kr'
        
    def render(self):
        # 언어 설정: 클래스의 lang 속성 우선 사용, 없으면 세션 상태에서 가져오기
        lang = self.lang
        if 'current_lang' in st.session_state:
            lang = st.session_state.current_lang
            
        status_type = st.session_state.get('view_equipment_status', 'error')
        
        # 상태 유형에 따른 제목 설정
        if status_type == "error":
            title = "고장/오류 설비 상세 현황"
        elif status_type == "pm":
            title = "설비 PM 진행 현황"
        elif status_type == "model_change":
            title = "모델 변경 진행 현황"
        else:
            title = "설비 상태 상세 현황"
            
        st.title(title)
        
        # 뒤로 가기 버튼
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
            
        # 샘플 데이터 생성
        equipment_data = self.get_sample_data(status_type)
        
        if equipment_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(equipment_data)
            
            # 상태 유형에 따른 열 정렬
            if status_type == "error":
                cols = ['equipment_number', 'location', 'error_code', 'error_desc', 'start_time', 'repair_status', 'assigned_to']
                col_names = {
                    'equipment_number': '설비 번호',
                    'location': '위치',
                    'error_code': '오류 코드',
                    'error_desc': '오류 내용',
                    'start_time': '발생 시간',
                    'repair_status': '수리 상태',
                    'assigned_to': '담당자'
                }
            elif status_type == "pm":
                cols = ['equipment_number', 'location', 'pm_type', 'start_time', 'end_time', 'progress', 'assigned_to']
                col_names = {
                    'equipment_number': '설비 번호',
                    'location': '위치',
                    'pm_type': 'PM 유형',
                    'start_time': '시작 시간',
                    'end_time': '예상 완료',
                    'progress': '진행률(%)',
                    'assigned_to': '담당자'
                }
            elif status_type == "model_change":
                cols = ['equipment_number', 'location', 'from_model', 'to_model', 'start_time', 'end_time', 'progress', 'assigned_to']
                col_names = {
                    'equipment_number': '설비 번호',
                    'location': '위치',
                    'from_model': '이전 모델',
                    'to_model': '변경 모델',
                    'start_time': '시작 시간',
                    'end_time': '예상 완료',
                    'progress': '진행률(%)',
                    'assigned_to': '담당자'
                }
            else:
                cols = df.columns.tolist()
                col_names = {col: col for col in cols}
                
            # 열 이름 변경
            df = df[cols].rename(columns=col_names)
            
            # 테이블 표시
            st.dataframe(df, use_container_width=True)
            
            # 작업별 액션 버튼 추가
            st.subheader("작업")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("담당자 변경", use_container_width=True):
                    st.info("담당자 변경 기능은 준비 중입니다.")
                    
            with col2:
                if status_type == "error":
                    button_text = "수리 완료 처리"
                elif status_type == "pm":
                    button_text = "PM 완료 처리"
                else:
                    button_text = "작업 완료 처리"
                    
                if st.button(button_text, use_container_width=True):
                    st.success("선택한 설비의 작업이 완료 처리되었습니다.")
                    
            with col3:
                if st.button("상세 이력 보기", use_container_width=True):
                    st.info("상세 이력 보기 기능은 준비 중입니다.")
        else:
            st.info(f"현재 {title}에 해당하는 설비가 없습니다.")
    
    def get_sample_data(self, status_type):
        """샘플 데이터 생성"""
        if status_type == "error":
            return [
                {
                    'equipment_number': 'EQ001', 
                    'location': 'A동 1라인',
                    'error_code': 'ERR-001',
                    'error_desc': '모터 과열',
                    'start_time': '2023-07-24 09:15',
                    'repair_status': '진행중',
                    'assigned_to': '김기술'
                },
                {
                    'equipment_number': 'EQ008', 
                    'location': 'B동 2라인',
                    'error_code': 'ERR-003',
                    'error_desc': '센서 오류',
                    'start_time': '2023-07-24 10:30',
                    'repair_status': '대기중',
                    'assigned_to': '이수리'
                },
            ]
        elif status_type == "pm":
            return [
                {
                    'equipment_number': 'EQ003', 
                    'location': 'A동 3라인',
                    'pm_type': '정기 점검',
                    'start_time': '2023-07-24 08:00',
                    'end_time': '2023-07-24 17:00',
                    'progress': 45,
                    'assigned_to': '박정비'
                },
                {
                    'equipment_number': 'EQ012', 
                    'location': 'C동 1라인',
                    'pm_type': '부품 교체',
                    'start_time': '2023-07-24 09:30',
                    'end_time': '2023-07-24 15:30',
                    'progress': 60,
                    'assigned_to': '최점검'
                },
            ]
        elif status_type == "model_change":
            return [
                {
                    'equipment_number': 'EQ005', 
                    'location': 'B동 1라인',
                    'from_model': 'A-100',
                    'to_model': 'B-200',
                    'start_time': '2023-07-24 07:30',
                    'end_time': '2023-07-24 14:30',
                    'progress': 75,
                    'assigned_to': '정모델'
                },
                {
                    'equipment_number': 'EQ015', 
                    'location': 'C동 3라인',
                    'from_model': 'X-50',
                    'to_model': 'X-60',
                    'start_time': '2023-07-24 10:00',
                    'end_time': '2023-07-24 16:00',
                    'progress': 30,
                    'assigned_to': '권변경'
                },
            ]
        else:
            return [] 