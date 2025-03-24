import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

def show_dashboard():
    st.title("Bảng điều khiển / 대시보드")
    
    # 날짜 필터
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Ngày bắt đầu / 시작일", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Ngày kết thúc / 종료일", datetime.now())
    
    # 예시 데이터 생성
    equipment_list = generate_equipment_data()
    error_history = generate_error_data(start_date, end_date)
    parts_history = generate_parts_data(start_date, end_date)
    
    # 데이터프레임 변환
    df_equipment = pd.DataFrame(equipment_list)
    df_errors = pd.DataFrame(error_history)
    df_parts = pd.DataFrame(parts_history)
    
    # 설비 상태 요약
    st.subheader("Tóm tắt trạng thái thiết bị / 설비 상태 요약")
    if not df_equipment.empty:
        status_counts = df_equipment['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Phân bố trạng thái thiết bị / 설비 상태 분포"
        )
        st.plotly_chart(fig_status)
    
    # 고장 통계
    st.subheader("Thống kê lỗi / 고장 통계")
    if not df_errors.empty:
        # 시간별 고장 건수
        df_errors['date'] = pd.to_datetime(df_errors['timestamp']).dt.date
        daily_errors = df_errors.groupby('date').size().reset_index(name='count')
        fig_errors = px.line(
            daily_errors,
            x='date',
            y='count',
            title="Số lượng lỗi hàng ngày / 일별 고장 건수",
            labels={'date': 'Ngày / 날짜', 'count': 'Số lượng / 건수'}
        )
        st.plotly_chart(fig_errors)
        
        # 고장 유형별 분포
        error_types = df_errors['error_code'].value_counts()
        fig_error_types = px.bar(
            x=error_types.index,
            y=error_types.values,
            title="Phân bố theo loại lỗi / 고장 유형별 분포",
            labels={'x': 'Mã lỗi / 오류 코드', 'y': 'Số lượng / 건수'}
        )
        st.plotly_chart(fig_error_types)
    
    # 부품 교체 통계
    st.subheader("Thống kê thay thế linh kiện / 부품 교체 통계")
    if not df_parts.empty:
        # 일별 부품 교체 건수
        df_parts['date'] = pd.to_datetime(df_parts['timestamp']).dt.date
        daily_parts = df_parts.groupby('date').size().reset_index(name='count')
        fig_parts = px.line(
            daily_parts,
            x='date',
            y='count',
            title="Số lượng thay thế linh kiện hàng ngày / 일별 부품 교체 건수",
            labels={'date': 'Ngày / 날짜', 'count': 'Số lượng / 건수'}
        )
        st.plotly_chart(fig_parts)
        
        # 부품별 교체 횟수
        parts_counts = df_parts['part_code'].value_counts()
        fig_parts_types = px.bar(
            x=parts_counts.index,
            y=parts_counts.values,
            title="Số lần thay thế theo linh kiện / 부품별 교체 횟수",
            labels={'x': 'Mã linh kiện / 부품 코드', 'y': 'Số lượng / 건수'}
        )
        st.plotly_chart(fig_parts_types)
    
    # 통계 요약
    st.subheader("Tóm tắt thống kê / 통계 요약")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Thời gian sửa chữa trung bình / 평균 수리 시간",
            f"{df_errors['repair_time'].mean():.1f} phút / 분"
        )
    with col2:
        st.metric(
            "Thời gian sửa chữa tối đa / 최대 수리 시간",
            f"{df_errors['repair_time'].max()} phút / 분"
        )
    with col3:
        st.metric(
            "Tổng thời gian dừng máy / 총 다운타임",
            f"{df_errors['repair_time'].sum()} phút / 분"
        )

# 예시 설비 데이터 생성
def generate_equipment_data():
    """설비 데이터 예시를 생성합니다."""
    equipment_data = [
        {
            'equipment_number': 'EQ001',
            'building': 'A동',
            'equipment_type': '프레스',
            'status': '정상 / Bình thường'
        },
        {
            'equipment_number': 'EQ002',
            'building': 'B동',
            'equipment_type': '컨베이어',
            'status': '점검중 / Đang kiểm tra'
        },
        {
            'equipment_number': 'EQ003',
            'building': 'A동',
            'equipment_type': '로봇',
            'status': '정상 / Bình thường'
        },
        {
            'equipment_number': 'EQ004',
            'building': 'C동',
            'equipment_type': '프레스',
            'status': '고장 / Hỏng'
        },
        {
            'equipment_number': 'EQ005',
            'building': 'B동',
            'equipment_type': '로봇',
            'status': '정상 / Bình thường'
        }
    ]
    return equipment_data

# 예시 고장 데이터 생성
def generate_error_data(start_date, end_date):
    """고장 데이터 예시를 생성합니다."""
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    error_codes = ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    workers = ['김철수', '이영희', '박민수', '정지원']
    
    error_data = []
    for _ in range(100):  # 100개의 오류 데이터 생성
        error_time = start_datetime + (end_datetime - start_datetime) * random.random()
        if start_date <= error_time.date() <= end_date:
            error_data.append({
                'timestamp': error_time,
                'equipment_number': random.choice(equipment_numbers),
                'error_code': random.choice(error_codes),
                'repair_time': random.randint(10, 120),
                'worker': random.choice(workers)
            })
    
    return error_data

# 예시 부품 데이터 생성
def generate_parts_data(start_date, end_date):
    """부품 교체 데이터 예시를 생성합니다."""
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    part_codes = ['P001', 'P002', 'P003', 'P004', 'P005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    workers = ['김철수', '이영희', '박민수', '정지원']
    
    parts_data = []
    for _ in range(50):  # 50개의 부품 교체 데이터 생성
        replace_time = start_datetime + (end_datetime - start_datetime) * random.random()
        if start_date <= replace_time.date() <= end_date:
            parts_data.append({
                'timestamp': replace_time,
                'equipment_number': random.choice(equipment_numbers),
                'part_code': random.choice(part_codes),
                'worker': random.choice(workers)
            })
    
    return parts_data 