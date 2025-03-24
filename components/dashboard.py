import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.supabase_client import (
    get_equipment_list,
    get_error_history,
    get_parts_replacement,
    get_error_stats,
    get_parts_stats
)

def show_dashboard():
    st.title("대시보드")
    
    # 날짜 필터
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("종료일", datetime.now())
    
    # 데이터 로드
    equipment_list = get_equipment_list()
    error_history = get_error_stats(start_date, end_date)
    parts_history = get_parts_stats(start_date, end_date)
    
    # 데이터프레임 변환
    df_equipment = pd.DataFrame(equipment_list)
    df_errors = pd.DataFrame(error_history)
    df_parts = pd.DataFrame(parts_history)
    
    # 설비 상태 요약
    st.subheader("설비 상태 요약")
    if not df_equipment.empty:
        status_counts = df_equipment['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="설비 상태 분포"
        )
        st.plotly_chart(fig_status)
    
    # 고장 통계
    st.subheader("고장 통계")
    if not df_errors.empty:
        # 시간별 고장 건수
        df_errors['date'] = pd.to_datetime(df_errors['timestamp']).dt.date
        daily_errors = df_errors.groupby('date').size().reset_index(name='count')
        fig_errors = px.line(
            daily_errors,
            x='date',
            y='count',
            title="일별 고장 건수"
        )
        st.plotly_chart(fig_errors)
        
        # 고장 유형별 분포
        error_types = df_errors['error_code'].value_counts()
        fig_error_types = px.bar(
            x=error_types.index,
            y=error_types.values,
            title="고장 유형별 분포"
        )
        st.plotly_chart(fig_error_types)
    
    # 부품 교체 통계
    st.subheader("부품 교체 통계")
    if not df_parts.empty:
        # 일별 부품 교체 건수
        df_parts['date'] = pd.to_datetime(df_parts['timestamp']).dt.date
        daily_parts = df_parts.groupby('date').size().reset_index(name='count')
        fig_parts = px.line(
            daily_parts,
            x='date',
            y='count',
            title="일별 부품 교체 건수"
        )
        st.plotly_chart(fig_parts)
        
        # 부품별 교체 횟수
        parts_counts = df_parts['part_code'].value_counts()
        fig_parts_types = px.bar(
            x=parts_counts.index,
            y=parts_counts.values,
            title="부품별 교체 횟수"
        )
        st.plotly_chart(fig_parts_types) 