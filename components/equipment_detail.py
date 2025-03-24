import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from components.language import get_text

# 추가 텍스트 정의
EQUIPMENT_TEXTS = {
    "equipment_detail": {
        "ko": "설비 상세 정보",
        "vi": "Chi tiết thiết bị"
    },
    "equipment_select": {
        "ko": "설비 선택",
        "vi": "Chọn thiết bị"
    },
    "equipment_number": {
        "ko": "설비 번호",
        "vi": "Số thiết bị"
    },
    "equipment_type": {
        "ko": "설비 유형",
        "vi": "Loại thiết bị"
    },
    "current_status": {
        "ko": "현재 상태",
        "vi": "Trạng thái hiện tại"
    },
    "error_history": {
        "ko": "고장 이력",
        "vi": "Lịch sử lỗi"
    },
    "no_error_history": {
        "ko": "고장 이력이 없습니다.",
        "vi": "Không có lịch sử lỗi"
    },
    "parts_history": {
        "ko": "부품 교체 이력",
        "vi": "Lịch sử thay thế linh kiện"
    },
    "no_parts_history": {
        "ko": "부품 교체 이력이 없습니다.",
        "vi": "Không có lịch sử thay thế linh kiện"
    },
    "occurrence_time": {
        "ko": "발생시간",
        "vi": "Thời gian xảy ra"
    },
    "error_code": {
        "ko": "에러 코드",
        "vi": "Mã lỗi"
    },
    "error_detail": {
        "ko": "에러 상세",
        "vi": "Chi tiết lỗi"
    },
    "repair_time": {
        "ko": "수리 시간",
        "vi": "Thời gian sửa chữa"
    },
    "repair_method": {
        "ko": "수리 방법",
        "vi": "Phương pháp sửa chữa"
    },
    "worker": {
        "ko": "작업자",
        "vi": "Người thực hiện"
    },
    "supervisor": {
        "ko": "관리자",
        "vi": "Người giám sát"
    },
    "replacement_time": {
        "ko": "교체시간",
        "vi": "Thời gian thay thế"
    },
    "part_code": {
        "ko": "부품 코드",
        "vi": "Mã linh kiện"
    }
}

def get_equipment_text(key, lang):
    """설비 상세 페이지 전용 텍스트를 가져옵니다."""
    if key in EQUIPMENT_TEXTS:
        return EQUIPMENT_TEXTS[key].get(lang, EQUIPMENT_TEXTS[key]['ko'])
    return f"[{key}]"

def show_equipment_detail(lang='ko'):
    """장비 상세 정보를 표시합니다."""
    st.title(get_equipment_text("equipment_detail", lang))
    
    # 설비 목록 로드 (예시 데이터 사용)
    equipment_list = generate_equipment_data(lang)
    
    # 설비 선택
    df_equipment = pd.DataFrame(equipment_list)
    selected_equipment = st.selectbox(
        get_equipment_text("equipment_select", lang),
        df_equipment['equipment_number'].tolist(),
        format_func=lambda x: f"{x} ({df_equipment[df_equipment['equipment_number'] == x]['equipment_type'].iloc[0]})"
    )
    
    if selected_equipment:
        # 선택된 설비 정보 표시
        equipment_info = df_equipment[df_equipment['equipment_number'] == selected_equipment].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(get_equipment_text("equipment_number", lang), equipment_info['equipment_number'])
        with col2:
            st.metric(get_equipment_text("equipment_type", lang), equipment_info['equipment_type'])
        with col3:
            st.metric(get_equipment_text("current_status", lang), equipment_info['status'])
        
        # 고장 이력
        st.subheader(get_equipment_text("error_history", lang))
        error_history = generate_error_history(lang)
        df_errors = pd.DataFrame(error_history)
        df_errors = df_errors[df_errors['equipment_number'] == selected_equipment]
        if not df_errors.empty:
            st.dataframe(
                df_errors,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn(
                        get_equipment_text("occurrence_time", lang),
                        format="YYYY-MM-DD HH:mm"
                    ),
                    "error_code": get_equipment_text("error_code", lang),
                    "error_detail": get_equipment_text("error_detail", lang),
                    "repair_time": get_equipment_text("repair_time", lang),
                    "repair_method": get_equipment_text("repair_method", lang),
                    "worker": get_equipment_text("worker", lang),
                    "supervisor": get_equipment_text("supervisor", lang)
                }
            )
        else:
            st.info(get_equipment_text("no_error_history", lang))
        
        # 부품 교체 이력
        st.subheader(get_equipment_text("parts_history", lang))
        parts_history = generate_parts_replacement(lang)
        df_parts = pd.DataFrame(parts_history)
        df_parts = df_parts[df_parts['equipment_number'] == selected_equipment]
        if not df_parts.empty:
            st.dataframe(
                df_parts,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn(
                        get_equipment_text("replacement_time", lang),
                        format="YYYY-MM-DD HH:mm"
                    ),
                    "part_code": get_equipment_text("part_code", lang),
                    "worker": get_equipment_text("worker", lang),
                    "supervisor": get_equipment_text("supervisor", lang)
                }
            )
        else:
            st.info(get_equipment_text("no_parts_history", lang))

# 예시 설비 데이터
def generate_equipment_data(lang='ko'):
    """설비 데이터 예시를 생성합니다."""
    buildings = {
        'ko': ['A동', 'B동', 'C동'],
        'vi': ['Tòa nhà A', 'Tòa nhà B', 'Tòa nhà C']
    }
    
    equipment_types = {
        'ko': ['프레스', '컨베이어', '로봇'],
        'vi': ['Máy ép', 'Băng tải', 'Robot']
    }
    
    equipment_data = [
        {
            'equipment_number': 'EQ001',
            'building': buildings[lang][0],
            'equipment_type': equipment_types[lang][0],
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ002',
            'building': buildings[lang][1],
            'equipment_type': equipment_types[lang][1],
            'status': get_text("inspection", lang)
        },
        {
            'equipment_number': 'EQ003',
            'building': buildings[lang][0],
            'equipment_type': equipment_types[lang][2],
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ004',
            'building': buildings[lang][2],
            'equipment_type': equipment_types[lang][0],
            'status': get_text("error", lang)
        },
        {
            'equipment_number': 'EQ005',
            'building': buildings[lang][1],
            'equipment_type': equipment_types[lang][2],
            'status': get_text("normal", lang)
        }
    ]
    return equipment_data

# 예시 고장 이력 데이터
def generate_error_history(lang='ko'):
    """고장 이력 예시를 생성합니다."""
    error_codes = ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    
    workers = {
        'ko': ['김철수', '이영희', '박민수', '정지원'],
        'vi': ['Kim Cheolsu', 'Lee Younghee', 'Park Minsu', 'Jung Jiwon']
    }
    
    repair_methods = {
        'ko': [
            '부품 교체', 
            '소프트웨어 재설정', 
            '센서 조정', 
            '전원 재시작', 
            '배선 교체'
        ],
        'vi': [
            'Thay thế linh kiện', 
            'Cài đặt lại phần mềm', 
            'Điều chỉnh cảm biến', 
            'Khởi động lại nguồn', 
            'Thay thế dây điện'
        ]
    }
    
    error_details = {
        'ko': '설비에서 발생한 오류',
        'vi': 'Lỗi phát sinh trên thiết bị'
    }
    
    supervisor = {
        'ko': '관리자',
        'vi': 'Quản lý'
    }
    
    error_data = []
    now = datetime.now()
    
    for i in range(50):  # 50개의 오류 데이터 생성
        equipment = random.choice(equipment_numbers)
        timestamp = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
        
        error_data.append({
            'timestamp': timestamp,
            'equipment_number': equipment,
            'error_code': random.choice(error_codes),
            'error_detail': f'{equipment} {error_details[lang]}',
            'repair_time': random.randint(10, 120),
            'repair_method': random.choice(repair_methods[lang]),
            'worker': random.choice(workers[lang]),
            'supervisor': supervisor[lang]
        })
    
    return error_data

# 예시 부품 교체 이력 데이터
def generate_parts_replacement(lang='ko'):
    """부품 교체 이력 예시를 생성합니다."""
    part_codes = ['P001', 'P002', 'P003', 'P004', 'P005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    
    workers = {
        'ko': ['김철수', '이영희', '박민수', '정지원'],
        'vi': ['Kim Cheolsu', 'Lee Younghee', 'Park Minsu', 'Jung Jiwon']
    }
    
    supervisor = {
        'ko': '관리자',
        'vi': 'Quản lý'
    }
    
    parts_data = []
    now = datetime.now()
    
    for i in range(30):  # 30개의 부품 교체 데이터 생성
        equipment = random.choice(equipment_numbers)
        timestamp = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
        
        parts_data.append({
            'timestamp': timestamp,
            'equipment_number': equipment,
            'part_code': random.choice(part_codes),
            'worker': random.choice(workers[lang]),
            'supervisor': supervisor[lang]
        })
    
    return parts_data 