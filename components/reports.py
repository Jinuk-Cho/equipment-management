import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """예시 데이터를 생성합니다."""
    # 현재 날짜를 기준으로 30일 전부터의 데이터 생성
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # 오류 이력 데이터
    error_codes = ['E001', 'E002', 'E003', 'E004', 'E005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004']
    workers = ['김철수 / Kim Cheolsu', '이영희 / Lee Younghee', '박민수 / Park Minsu', '정지원 / Jung Jiwon']
    
    error_data = []
    for _ in range(100):  # 100개의 오류 데이터 생성
        error_time = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        error_data.append({
            '발생시간': error_time,
            '설비번호': random.choice(equipment_numbers),
            '오류코드': random.choice(error_codes),
            '수리시간': random.randint(10, 120),
            '작업자': random.choice(workers)
        })
    
    # 부품 교체 데이터
    part_codes = ['P001', 'P002', 'P003', 'P004']
    
    parts_data = []
    for _ in range(50):  # 50개의 부품 교체 데이터 생성
        replacement_time = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        parts_data.append({
            '교체시간': replacement_time,
            '설비번호': random.choice(equipment_numbers),
            '부품코드': random.choice(part_codes),
            '작업자': random.choice(workers)
        })
    
    return pd.DataFrame(error_data), pd.DataFrame(parts_data)

def show_reports():
    """보고서 및 통계 페이지를 표시합니다."""
    st.title("Báo cáo và thống kê / 보고서 및 통계")
    
    # 예시 데이터 생성
    error_history, parts_history = generate_sample_data()
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "Phân tích loại lỗi / 고장 유형 분석",
        "Tình trạng tiêu thụ linh kiện / 부품 소모 현황",
        "Thống kê theo người thực hiện / 작업자별 통계",
        "Phân tích thời gian ngừng máy / 다운타임 분석"
    ])
    
    # 고장 유형 분석
    with tab1:
        st.subheader("Số lần xuất hiện theo mã lỗi / 오류 코드별 발생 횟수")
        error_counts = error_history['오류코드'].value_counts()
        
        fig = px.bar(
            x=error_counts.index,
            y=error_counts.values,
            labels={'x': 'Mã lỗi / 오류 코드', 'y': 'Số lần xuất hiện / 발생 횟수'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 시간대별 고장 발생 추이
        error_history['시간'] = pd.to_datetime(error_history['발생시간']).dt.hour
        hourly_errors = error_history['시간'].value_counts().sort_index()
        
        fig = px.line(
            x=hourly_errors.index,
            y=hourly_errors.values,
            labels={'x': 'Giờ / 시간', 'y': 'Số lần xuất hiện / 발생 횟수'},
            title="Xu hướng xuất hiện lỗi theo giờ / 시간대별 고장 발생 추이"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 부품 소모 현황
    with tab2:
        st.subheader("Số lần thay thế theo linh kiện / 부품별 교체 횟수")
        parts_counts = parts_history['부품코드'].value_counts()
        
        fig = px.pie(
            values=parts_counts.values,
            names=parts_counts.index,
            title="Tỷ lệ thay thế theo linh kiện / 부품별 교체 비율"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 월별 부품 교체 추이
        parts_history['월'] = pd.to_datetime(parts_history['교체시간']).dt.strftime('%Y-%m')
        monthly_parts = parts_history.groupby('월')['부품코드'].count()
        
        fig = px.line(
            x=monthly_parts.index,
            y=monthly_parts.values,
            labels={'x': 'Tháng / 월', 'y': 'Số lần thay thế / 교체 횟수'},
            title="Xu hướng thay thế linh kiện theo tháng / 월별 부품 교체 추이"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 작업자별 통계
    with tab3:
        st.subheader("Số lượng xử lý theo người thực hiện / 작업자별 처리 건수")
        worker_counts = error_history['작업자'].value_counts()
        
        fig = px.bar(
            x=worker_counts.index,
            y=worker_counts.values,
            labels={'x': 'Người thực hiện / 작업자', 'y': 'Số lượng xử lý / 처리 건수'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 작업자별 평균 수리 시간
        worker_times = error_history.groupby('작업자')['수리시간'].mean()
        
        fig = px.bar(
            x=worker_times.index,
            y=worker_times.values,
            labels={'x': 'Người thực hiện / 작업자', 'y': 'Thời gian sửa chữa trung bình (phút) / 평균 수리 시간 (분)'},
            title="Thời gian sửa chữa trung bình theo người thực hiện / 작업자별 평균 수리 시간"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 다운타임 분석
    with tab4:
        st.subheader("Thời gian ngừng máy theo thiết bị / 설비별 다운타임")
        equipment_downtime = error_history.groupby('설비번호')['수리시간'].sum()
        
        fig = px.bar(
            x=equipment_downtime.index,
            y=equipment_downtime.values,
            labels={'x': 'Số thiết bị / 설비 번호', 'y': 'Tổng thời gian ngừng máy (phút) / 총 다운타임 (분)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 오류 코드별 평균 수리 시간
        error_repair_time = error_history.groupby('오류코드')['수리시간'].mean()
        
        fig = px.bar(
            x=error_repair_time.index,
            y=error_repair_time.values,
            labels={'x': 'Mã lỗi / 오류 코드', 'y': 'Thời gian sửa chữa trung bình (phút) / 평균 수리 시간 (분)'},
            title="Thời gian sửa chữa trung bình theo mã lỗi / 오류 코드별 평균 수리 시간"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 통계 요약
        st.subheader("Tóm tắt thống kê / 통계 요약")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Thời gian sửa chữa trung bình / 평균 수리 시간",
                f"{error_history['수리시간'].mean():.1f} phút / 분"
            )
        with col2:
            st.metric(
                "Thời gian sửa chữa tối đa / 최대 수리 시간",
                f"{error_history['수리시간'].max()} phút / 분"
            )
        with col3:
            st.metric(
                "Tổng thời gian ngừng máy / 총 다운타임",
                f"{error_history['수리시간'].sum()} phút / 분"
            ) 