import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def show_equipment_detail():
    """장비 상세 정보를 표시합니다."""
    st.title("Chi tiết thiết bị / 설비 상세 정보")
    
    # 설비 목록 로드 (예시 데이터 사용)
    equipment_list = generate_equipment_data()
    
    # 설비 선택
    df_equipment = pd.DataFrame(equipment_list)
    selected_equipment = st.selectbox(
        "Chọn thiết bị / 설비 선택",
        df_equipment['equipment_number'].tolist(),
        format_func=lambda x: f"{x} ({df_equipment[df_equipment['equipment_number'] == x]['equipment_type'].iloc[0]})"
    )
    
    if selected_equipment:
        # 선택된 설비 정보 표시
        equipment_info = df_equipment[df_equipment['equipment_number'] == selected_equipment].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Số thiết bị / 설비 번호", equipment_info['equipment_number'])
        with col2:
            st.metric("Loại thiết bị / 설비 유형", equipment_info['equipment_type'])
        with col3:
            st.metric("Trạng thái hiện tại / 현재 상태", equipment_info['status'])
        
        # 고장 이력
        st.subheader("Lịch sử lỗi / 고장 이력")
        error_history = generate_error_history()
        df_errors = pd.DataFrame(error_history)
        df_errors = df_errors[df_errors['equipment_number'] == selected_equipment]
        if not df_errors.empty:
            st.dataframe(
                df_errors,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn(
                        "Thời gian xảy ra / 발생시간",
                        format="YYYY-MM-DD HH:mm"
                    ),
                    "error_code": "Mã lỗi / 에러 코드",
                    "error_detail": "Chi tiết lỗi / 에러 상세",
                    "repair_time": "Thời gian sửa chữa / 수리 시간",
                    "repair_method": "Phương pháp sửa chữa / 수리 방법",
                    "worker": "Người thực hiện / 작업자",
                    "supervisor": "Người giám sát / 관리자"
                }
            )
        else:
            st.info("Không có lịch sử lỗi / 고장 이력이 없습니다.")
        
        # 부품 교체 이력
        st.subheader("Lịch sử thay thế linh kiện / 부품 교체 이력")
        parts_history = generate_parts_replacement()
        df_parts = pd.DataFrame(parts_history)
        df_parts = df_parts[df_parts['equipment_number'] == selected_equipment]
        if not df_parts.empty:
            st.dataframe(
                df_parts,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn(
                        "Thời gian thay thế / 교체시간",
                        format="YYYY-MM-DD HH:mm"
                    ),
                    "part_code": "Mã linh kiện / 부품 코드",
                    "worker": "Người thực hiện / 작업자",
                    "supervisor": "Người giám sát / 관리자"
                }
            )
        else:
            st.info("Không có lịch sử thay thế linh kiện / 부품 교체 이력이 없습니다.")

# 예시 설비 데이터
def generate_equipment_data():
    """설비 데이터 예시를 생성합니다."""
    equipment_data = [
        {
            'equipment_number': 'EQ001',
            'building': 'Tòa nhà A / A동',
            'equipment_type': 'Máy ép / 프레스',
            'status': 'Bình thường / 정상'
        },
        {
            'equipment_number': 'EQ002',
            'building': 'Tòa nhà B / B동',
            'equipment_type': 'Băng tải / 컨베이어',
            'status': 'Đang kiểm tra / 점검중'
        },
        {
            'equipment_number': 'EQ003',
            'building': 'Tòa nhà A / A동',
            'equipment_type': 'Robot / 로봇',
            'status': 'Bình thường / 정상'
        },
        {
            'equipment_number': 'EQ004',
            'building': 'Tòa nhà C / C동',
            'equipment_type': 'Máy ép / 프레스',
            'status': 'Hỏng / 고장'
        },
        {
            'equipment_number': 'EQ005',
            'building': 'Tòa nhà B / B동',
            'equipment_type': 'Robot / 로봇',
            'status': 'Bình thường / 정상'
        }
    ]
    return equipment_data

# 예시 고장 이력 데이터
def generate_error_history():
    """고장 이력 예시를 생성합니다."""
    error_codes = ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    workers = ['김철수 / Kim Cheolsu', '이영희 / Lee Younghee', '박민수 / Park Minsu', '정지원 / Jung Jiwon']
    repair_methods = [
        'Thay thế linh kiện / 부품 교체', 
        'Cài đặt lại phần mềm / 소프트웨어 재설정', 
        'Điều chỉnh cảm biến / 센서 조정', 
        'Khởi động lại nguồn / 전원 재시작', 
        'Thay thế dây điện / 배선 교체'
    ]
    
    error_data = []
    now = datetime.now()
    
    for i in range(50):  # 50개의 오류 데이터 생성
        equipment = random.choice(equipment_numbers)
        timestamp = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
        
        error_data.append({
            'timestamp': timestamp,
            'equipment_number': equipment,
            'error_code': random.choice(error_codes),
            'error_detail': f'Lỗi phát sinh trên thiết bị {equipment} / {equipment} 설비에서 발생한 오류',
            'repair_time': random.randint(10, 120),
            'repair_method': random.choice(repair_methods),
            'worker': random.choice(workers),
            'supervisor': 'Quản lý / 관리자' 
        })
    
    return error_data

# 예시 부품 교체 이력 데이터
def generate_parts_replacement():
    """부품 교체 이력 예시를 생성합니다."""
    part_codes = ['P001', 'P002', 'P003', 'P004', 'P005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    workers = ['김철수 / Kim Cheolsu', '이영희 / Lee Younghee', '박민수 / Park Minsu', '정지원 / Jung Jiwon']
    
    parts_data = []
    now = datetime.now()
    
    for i in range(30):  # 30개의 부품 교체 데이터 생성
        equipment = random.choice(equipment_numbers)
        timestamp = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
        
        parts_data.append({
            'timestamp': timestamp,
            'equipment_number': equipment,
            'part_code': random.choice(part_codes),
            'worker': random.choice(workers),
            'supervisor': 'Quản lý / 관리자'
        })
    
    return parts_data 