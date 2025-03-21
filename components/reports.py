import streamlit as st
import pandas as pd
import plotly.express as px
from utils.google_sheet import get_sheet_data

def show_reports():
    """보고서 및 통계 페이지를 표시합니다."""
    st.title("보고서 및 통계")
    
    if 'credentials' not in st.session_state:
        st.error("Google 계정 인증이 필요합니다.")
        return
    
    # 데이터 가져오기
    error_history = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "오류이력!A1:H"
    )
    
    parts_history = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "부품교체!A1:E"
    )
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "고장 유형 분석",
        "부품 소모 현황",
        "작업자별 통계",
        "다운타임 분석"
    ])
    
    # 고장 유형 분석
    with tab1:
        st.subheader("오류 코드별 발생 횟수")
        error_counts = error_history['오류코드'].value_counts()
        
        fig = px.bar(
            x=error_counts.index,
            y=error_counts.values,
            labels={'x': '오류 코드', 'y': '발생 횟수'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 시간대별 고장 발생 추이
        error_history['시간'] = pd.to_datetime(error_history['발생시간']).dt.hour
        hourly_errors = error_history['시간'].value_counts().sort_index()
        
        fig = px.line(
            x=hourly_errors.index,
            y=hourly_errors.values,
            labels={'x': '시간', 'y': '발생 횟수'},
            title="시간대별 고장 발생 추이"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 부품 소모 현황
    with tab2:
        st.subheader("부품별 교체 횟수")
        parts_counts = parts_history['부품코드'].value_counts()
        
        fig = px.pie(
            values=parts_counts.values,
            names=parts_counts.index,
            title="부품별 교체 비율"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 월별 부품 교체 추이
        parts_history['월'] = pd.to_datetime(parts_history['교체시간']).dt.strftime('%Y-%m')
        monthly_parts = parts_history.groupby('월')['부품코드'].count()
        
        fig = px.line(
            x=monthly_parts.index,
            y=monthly_parts.values,
            labels={'x': '월', 'y': '교체 횟수'},
            title="월별 부품 교체 추이"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 작업자별 통계
    with tab3:
        st.subheader("작업자별 처리 건수")
        worker_counts = error_history['작업자'].value_counts()
        
        fig = px.bar(
            x=worker_counts.index,
            y=worker_counts.values,
            labels={'x': '작업자', 'y': '처리 건수'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 작업자별 평균 수리 시간
        worker_times = error_history.groupby('작업자')['수리시간'].mean()
        
        fig = px.bar(
            x=worker_times.index,
            y=worker_times.values,
            labels={'x': '작업자', 'y': '평균 수리 시간 (분)'},
            title="작업자별 평균 수리 시간"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 다운타임 분석
    with tab4:
        st.subheader("설비별 다운타임")
        equipment_downtime = error_history.groupby('설비번호')['수리시간'].sum()
        
        fig = px.bar(
            x=equipment_downtime.index,
            y=equipment_downtime.values,
            labels={'x': '설비 번호', 'y': '총 다운타임 (분)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 오류 코드별 평균 수리 시간
        error_repair_time = error_history.groupby('오류코드')['수리시간'].mean()
        
        fig = px.bar(
            x=error_repair_time.index,
            y=error_repair_time.values,
            labels={'x': '오류 코드', 'y': '평균 수리 시간 (분)'},
            title="오류 코드별 평균 수리 시간"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 통계 요약
        st.subheader("통계 요약")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "평균 수리 시간",
                f"{error_history['수리시간'].mean():.1f}분"
            )
        with col2:
            st.metric(
                "최대 수리 시간",
                f"{error_history['수리시간'].max()}분"
            )
        with col3:
            st.metric(
                "총 다운타임",
                f"{error_history['수리시간'].sum()}분"
            ) 