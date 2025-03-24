import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random
from components.language import get_text

def show_dashboard(lang='ko'):
    """대시보드를 표시합니다."""
    # 예시 데이터 생성
    equipment_list = generate_equipment_data(lang)
    error_history = generate_error_data(datetime.now() - timedelta(days=30), datetime.now())
    parts_history = generate_parts_data(datetime.now() - timedelta(days=30), datetime.now())
    
    # 데이터프레임 변환
    df_equipment = pd.DataFrame(equipment_list)
    df_errors = pd.DataFrame(error_history)
    df_parts = pd.DataFrame(parts_history)
    
    # 2x2 그리드 레이아웃
    col1, col2 = st.columns(2)
    
    # 첫 번째 열
    with col1:
        # 설비 상태 요약
        if not df_equipment.empty:
            status_counts = df_equipment['status'].value_counts()
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title=get_text("equipment_status_distribution", lang),
                height=300
            )
            fig_status.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_status, use_container_width=True)
        
        # 고장 유형별 분포
        if not df_errors.empty:
            error_types = df_errors['error_code'].value_counts()
            fig_error_types = px.bar(
                x=error_types.index,
                y=error_types.values,
                title=get_text("error_distribution", lang),
                labels={
                    'x': get_text("error_code", lang), 
                    'y': get_text("count", lang)
                },
                height=300
            )
            fig_error_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_error_types, use_container_width=True)
    
    # 두 번째 열
    with col2:
        # 시간별 고장 건수
        if not df_errors.empty:
            df_errors['date'] = pd.to_datetime(df_errors['timestamp']).dt.date
            daily_errors = df_errors.groupby('date').size().reset_index(name='count')
            fig_errors = px.line(
                daily_errors,
                x='date',
                y='count',
                title=get_text("daily_errors", lang),
                labels={
                    'date': get_text("date", lang), 
                    'count': get_text("count", lang)
                },
                height=300
            )
            fig_errors.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_errors, use_container_width=True)
        
        # 부품별 교체 횟수
        if not df_parts.empty:
            parts_counts = df_parts['part_code'].value_counts()
            fig_parts_types = px.bar(
                x=parts_counts.index,
                y=parts_counts.values,
                title=get_text("parts_replacement", lang),
                labels={
                    'x': get_text("part_code", lang), 
                    'y': get_text("count", lang)
                },
                height=300
            )
            fig_parts_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_parts_types, use_container_width=True)
    
    # 통계 요약 - 하단에 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            get_text("average_repair_time", lang),
            f"{df_errors['repair_time'].mean():.1f} {get_text('minutes', lang)}"
        )
    with col2:
        st.metric(
            get_text("max_repair_time", lang),
            f"{df_errors['repair_time'].max()} {get_text('minutes', lang)}"
        )
    with col3:
        st.metric(
            get_text("total_downtime", lang),
            f"{df_errors['repair_time'].sum()} {get_text('minutes', lang)}"
        )

def generate_equipment_data(lang='ko'):
    """설비 데이터 예시를 생성합니다."""
    equipment_data = [
        {
            'equipment_number': 'EQ001',
            'building': 'A동',
            'equipment_type': '프레스',
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ002',
            'building': 'B동',
            'equipment_type': '컨베이어',
            'status': get_text("inspection", lang)
        },
        {
            'equipment_number': 'EQ003',
            'building': 'A동',
            'equipment_type': '로봇',
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ004',
            'building': 'C동',
            'equipment_type': '프레스',
            'status': get_text("error", lang)
        },
        {
            'equipment_number': 'EQ005',
            'building': 'B동',
            'equipment_type': '로봇',
            'status': get_text("normal", lang)
        }
    ]
    return equipment_data

def generate_error_data(start_date, end_date):
    """고장 데이터 예시를 생성합니다."""
    error_data = []
    for _ in range(50):
        timestamp = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        error_data.append({
            'timestamp': timestamp,
            'equipment_number': f'EQ00{random.randint(1, 5)}',
            'error_code': f'E00{random.randint(1, 5)}',
            'repair_time': random.randint(10, 120)
        })
    return error_data

def generate_parts_data(start_date, end_date):
    """부품 교체 데이터 예시를 생성합니다."""
    parts_data = []
    for _ in range(30):
        timestamp = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        parts_data.append({
            'timestamp': timestamp,
            'equipment_number': f'EQ00{random.randint(1, 5)}',
            'part_code': f'P00{random.randint(1, 4)}'
        })
    return parts_data 