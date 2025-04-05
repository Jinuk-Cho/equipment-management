"""
보고서 관련 차트 및 시각화를 위한 모듈
- 오류 유형별 분석 차트
- 오류 코드별 발생 횟수 바 차트
- 시간대별 오류 발생 추이 라인 차트
- 작업자별 처리 건수 바 차트
- 작업자별 평균 수리 시간 바 차트
- 설비별 다운타임 바 차트
- 오류 코드별 평균 수리 시간 바 차트
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from components.language import get_text
import random

def render_error_code_bar_chart(error_data, lang='ko'):
    """
    오류 코드별 발생 횟수를 바 차트로 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 오류 코드별 발생 횟수 집계
    error_counts = error_data['오류코드'].value_counts().reset_index()
    error_counts.columns = [get_text("error_code", lang), get_text("occurrences", lang)]
    
    # 바 차트 생성
    fig_error_counts = px.bar(
        error_counts,
        x=get_text("error_code", lang),
        y=get_text("occurrences", lang),
        title=get_text("occurrences_by_error_code", lang)
    )
    
    # 차트 표시
    st.plotly_chart(fig_error_counts, use_container_width=True)

def render_error_trend_by_hour(error_data, lang='ko'):
    """
    시간대별 오류 발생 추이를 라인 차트로 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 시간대별 오류 발생 횟수 집계
    hour_counts = error_data['시간'].value_counts().reset_index()
    hour_counts.columns = [get_text("hour", lang), get_text("occurrences", lang)]
    hour_counts = hour_counts.sort_values(by=get_text("hour", lang))
    
    # 라인 차트 생성
    fig_hour_trend = px.line(
        hour_counts,
        x=get_text("hour", lang),
        y=get_text("occurrences", lang),
        title=get_text("error_trend_by_hour", lang),
        markers=True
    )
    
    # 차트 표시
    st.plotly_chart(fig_hour_trend, use_container_width=True)

def render_worker_bar_charts(error_data, lang='ko'):
    """
    작업자별 처리 건수 및 평균 수리 시간을 바 차트로 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 작업자별 처리 건수 집계
    worker_counts = error_data['작업자'].value_counts().reset_index()
    worker_counts.columns = [get_text("worker", lang), get_text("occurrences", lang)]
    
    # 처리 건수 바 차트 생성
    fig_worker_counts = px.bar(
        worker_counts,
        x=get_text("worker", lang),
        y=get_text("occurrences", lang),
        title=get_text("occurrences_by_worker", lang)
    )
    
    # 차트 표시
    st.plotly_chart(fig_worker_counts, use_container_width=True)
    
    # 작업자별 평균 수리 시간 집계
    worker_repair_times = error_data.groupby('작업자')['수리시간'].mean().reset_index()
    worker_repair_times.columns = [get_text("worker", lang), get_text("avg_repair_time", lang)]
    
    # 평균 수리 시간 바 차트 생성
    fig_worker_times = px.bar(
        worker_repair_times,
        x=get_text("worker", lang),
        y=get_text("avg_repair_time", lang),
        title=get_text("avg_repair_time_by_worker", lang)
    )
    
    # 차트 표시
    st.plotly_chart(fig_worker_times, use_container_width=True)

def render_equipment_downtime_bar_chart(error_data, lang='ko'):
    """
    설비별 다운타임을 바 차트로 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 설비별 다운타임 집계
    equipment_downtime = error_data.groupby('설비번호')['수리시간'].sum().reset_index()
    equipment_downtime.columns = [get_text("equipment_number", lang), get_text("downtime", lang)]
    
    # 다운타임 바 차트 생성
    fig_downtime = px.bar(
        equipment_downtime,
        x=get_text("equipment_number", lang),
        y=get_text("downtime", lang),
        title=get_text("downtime_by_equipment", lang)
    )
    
    # 차트 표시
    st.plotly_chart(fig_downtime, use_container_width=True)

def render_error_repair_time_bar_chart(error_data, lang='ko'):
    """
    오류 코드별 평균 수리 시간을 바 차트로 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 오류 코드별 평균 수리 시간 집계
    error_repair_times = error_data.groupby('오류코드')['수리시간'].mean().reset_index()
    error_repair_times.columns = [get_text("error_code", lang), get_text("avg_repair_time", lang)]
    
    # 평균 수리 시간 바 차트 생성
    fig_error_times = px.bar(
        error_repair_times,
        x=get_text("error_code", lang),
        y=get_text("avg_repair_time", lang),
        title=get_text("avg_repair_time_by_error", lang)
    )
    
    # 차트 표시
    st.plotly_chart(fig_error_times, use_container_width=True)

def render_repair_time_summary_metrics(error_data, lang='ko'):
    """
    수리 시간 관련 요약 지표를 표시합니다.
    
    Args:
        error_data (pd.DataFrame): 오류 데이터프레임
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 지표는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if error_data.empty:
        st.info(get_text("no_error_data", lang))
        return
    
    # 3개 열로 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 평균 수리 시간
        st.metric(
            get_text("average_repair_time", lang),
            f"{error_data['수리시간'].mean():.1f} {get_text('minutes', lang)}"
        )
    
    with col2:
        # 최대 수리 시간
        st.metric(
            get_text("max_repair_time", lang),
            f"{error_data['수리시간'].max()} {get_text('minutes', lang)}"
        )
    
    with col3:
        # 총 다운타임
        st.metric(
            get_text("total_downtime", lang),
            f"{error_data['수리시간'].sum()} {get_text('minutes', lang)}"
        ) 