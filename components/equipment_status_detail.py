import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from components.language import _normalize_language_code, get_text

class EquipmentStatusDetailComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'ko'
    
    def render(self):
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
            
        # 상태 유형 가져오기 (error, pm, model_change)
        status_type = st.session_state.get('view_equipment_status', 'error')
        
        # 상태 유형에 따른 제목 설정
        if status_type == 'error':
            title = "오류 상태 상세"
        elif status_type == 'pm':
            title = "PM 상세"
        elif status_type == 'model_change':
            title = "모델 변경 상세"
        else:
            title = "설비 상태 상세"
        
        st.subheader(title)
        
        # 뒤로 가기 버튼
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.experimental_rerun()
        
        # 선택된 상태 유형에 맞는 데이터 생성
        equipment_data = self.get_sample_data(status_type, lang)
        
        if equipment_data:
            df = pd.DataFrame(equipment_data)
            
            # 헤더 한글화
            korean_columns = {
                'equipment_number': '설비번호',
                'building': '건물',
                'equipment_type': '설비타입',
                'status': '상태',
                'error_code': '오류코드',
                'error_detail': '오류내용',
                'pm_date': 'PM예정일',
                'pm_type': 'PM유형',
                'model_change_date': '모델변경일',
                'worker': '담당자'
            }
            
            df = df.rename(columns=korean_columns)
            
            # 표 표시
            st.dataframe(df, use_container_width=True)
            
            # 선택된 행에 대한 작업
            selected_indices = st.multiselect('작업할 설비를 선택하세요', df.index)
            
            if selected_indices:
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("담당자 변경"):
                        st.success(f"{len(selected_indices)}개 설비의 담당자가 변경되었습니다.")
                
                with action_col2:
                    if st.button("작업 완료 처리"):
                        st.success(f"{len(selected_indices)}개 설비의 작업이 완료 처리되었습니다.")
                
                with action_col3:
                    if st.button("상세 이력 보기"):
                        st.info("상세 이력 페이지로 이동합니다.")
        else:
            st.warning("표시할 설비 데이터가 없습니다.")
    
    def get_sample_data(self, status_type, lang):
        """샘플 데이터 생성"""
        # 언어 코드 표준화
        normalized_lang = _normalize_language_code(lang)
        
        # 건물 및 설비 타입 데이터
        buildings = {
            'ko': ['1공장', '2공장', '3공장', '물류센터'],
            'vi': ['Factory 1', 'Factory 2', 'Factory 3', 'Logistics Center']
        }
        
        equipment_types = {
            'ko': ['조립기', '검사기', '프레스', '컨베이어', '로봇'],
            'vi': ['Assembler', 'Tester', 'Press', 'Conveyor', 'Robot']
        }
        
        workers = {
            'ko': ['김철수', '이영희', '박민수', '정지원', '최영수'],
            'vi': ['Kim', 'Lee', 'Park', 'Jung', 'Choi']
        }
        
        # 기본값 설정 (언어 코드가 잘못된 경우 한국어 사용)
        building_list = buildings.get(normalized_lang, buildings['ko'])
        equipment_type_list = equipment_types.get(normalized_lang, equipment_types['ko'])
        worker_list = workers.get(normalized_lang, workers['ko'])
        
        # 상태 유형에 따른 데이터 생성
        data = []
        
        if status_type == 'error':
            error_codes = ['E001', 'E002', 'E003', 'E004']
            error_details = {
                'ko': {
                    'E001': '센서 오류',
                    'E002': '모터 과부하',
                    'E003': '통신 오류',
                    'E004': '전원 불안정'
                },
                'vi': {
                    'E001': 'Sensor Error',
                    'E002': 'Motor Overload',
                    'E003': 'Communication Error',
                    'E004': 'Power Instability'
                }
            }
            
            for i in range(10):
                error_code = random.choice(error_codes)
                data.append({
                    'equipment_number': f'EQ{random.randint(100, 999)}',
                    'building': random.choice(building_list),
                    'equipment_type': random.choice(equipment_type_list),
                    'status': '오류' if normalized_lang == 'ko' else 'Error',
                    'error_code': error_code,
                    'error_detail': error_details.get(normalized_lang, error_details['ko'])[error_code],
                    'worker': random.choice(worker_list)
                })
                
        elif status_type == 'pm':
            pm_types = {
                'ko': ['정기 점검', '부품 교체', '소프트웨어 업데이트'],
                'vi': ['Regular Check', 'Parts Replacement', 'Software Update']
            }
            
            pm_type_list = pm_types.get(normalized_lang, pm_types['ko'])
            
            for i in range(10):
                future_date = datetime.now() + timedelta(days=random.randint(1, 30))
                data.append({
                    'equipment_number': f'EQ{random.randint(100, 999)}',
                    'building': random.choice(building_list),
                    'equipment_type': random.choice(equipment_type_list),
                    'status': 'PM 예정' if normalized_lang == 'ko' else 'PM Scheduled',
                    'pm_date': future_date.strftime('%Y-%m-%d'),
                    'pm_type': random.choice(pm_type_list),
                    'worker': random.choice(worker_list)
                })
                
        elif status_type == 'model_change':
            for i in range(10):
                future_date = datetime.now() + timedelta(days=random.randint(1, 15))
                data.append({
                    'equipment_number': f'EQ{random.randint(100, 999)}',
                    'building': random.choice(building_list),
                    'equipment_type': random.choice(equipment_type_list),
                    'status': '모델 변경 예정' if normalized_lang == 'ko' else 'Model Change Scheduled',
                    'model_change_date': future_date.strftime('%Y-%m-%d'),
                    'worker': random.choice(worker_list)
                })
                
        return data 