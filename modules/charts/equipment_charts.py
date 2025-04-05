"""
장비 관련 차트 및 시각화를 위한 모듈
- 장비 상태 분포 파이 차트
- 고장 유형별 분포 바 차트
- 시간별 고장 건수 라인 차트
- 부품별 교체 횟수 바 차트
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from components.language import get_text
import random

def render_equipment_status_pie_chart(equipment_data, lang='ko'):
    """
    장비 상태 분포를 파이 차트로 표시합니다.
    
    Args:
        equipment_data (list): 장비 데이터 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if not equipment_data:
        st.info(get_text("no_equipment_data", lang))
        return
    
    df_equipment = pd.DataFrame(equipment_data)
    
    # 상태 분포 계산
    status_counts = df_equipment['status'].value_counts()
    
    # 파이 차트 생성
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title=get_text("equipment_status_distribution", lang),
        height=300
    )
    
    # 차트 레이아웃 조정
    fig_status.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    
    # 차트 표시
    st.plotly_chart(fig_status, use_container_width=True)

def render_error_type_bar_chart(error_data, lang='ko'):
    """
    오류 코드별 분포를 바 차트로 표시합니다.
    
    Args:
        error_data (list): 오류 데이터 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if not error_data:
        st.info(get_text("no_error_data", lang))
        return
    
    df_errors = pd.DataFrame(error_data)
    
    # 오류 유형별 건수 계산
    error_types = df_errors['error_code'].value_counts()
    
    # 바 차트 생성
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
    
    # 차트 레이아웃 조정
    fig_error_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    
    # 차트 표시
    st.plotly_chart(fig_error_types, use_container_width=True)

def render_daily_errors_line_chart(error_data, lang='ko'):
    """
    일별 오류 발생 추이를 라인 차트로 표시합니다.
    
    Args:
        error_data (list): 오류 데이터 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if not error_data:
        st.info(get_text("no_error_data", lang))
        return
    
    df_errors = pd.DataFrame(error_data)
    
    # 날짜 형식 변환
    df_errors['date'] = pd.to_datetime(df_errors['timestamp']).dt.date
    
    # 일별 오류 건수 집계
    daily_errors = df_errors.groupby('date').size().reset_index(name='count')
    
    # 라인 차트 생성
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
    
    # 차트 레이아웃 조정
    fig_errors.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    
    # 차트 표시
    st.plotly_chart(fig_errors, use_container_width=True)

def render_parts_replacement_bar_chart(parts_data, lang='ko'):
    """
    부품별 교체 횟수를 바 차트로 표시합니다.
    
    Args:
        parts_data (list): 부품 교체 데이터 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 차트는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if not parts_data:
        st.info(get_text("no_parts_data", lang))
        return
    
    df_parts = pd.DataFrame(parts_data)
    
    # 부품별 교체 횟수 집계
    parts_counts = df_parts['part_code'].value_counts()
    
    # 바 차트 생성
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
    
    # 차트 레이아웃 조정
    fig_parts_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    
    # 차트 표시
    st.plotly_chart(fig_parts_types, use_container_width=True)

def render_repair_time_metrics(error_data, lang='ko'):
    """
    수리 시간 관련 지표를 표시합니다.
    
    Args:
        error_data (list): 오류 데이터 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 지표는 streamlit을 통해 직접 화면에 표시됩니다.
    """
    if not error_data:
        st.info(get_text("no_error_data", lang))
        return
    
    df_errors = pd.DataFrame(error_data)
    
    # 3개 열로 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 평균 수리 시간
        st.metric(
            get_text("average_repair_time", lang),
            f"{df_errors['repair_time'].mean():.1f} {get_text('minutes', lang)}"
        )
    
    with col2:
        # 최대 수리 시간
        st.metric(
            get_text("max_repair_time", lang),
            f"{df_errors['repair_time'].max()} {get_text('minutes', lang)}"
        )
    
    with col3:
        # 총 다운타임
        st.metric(
            get_text("total_downtime", lang),
            f"{df_errors['repair_time'].sum()} {get_text('minutes', lang)}"
        ) 