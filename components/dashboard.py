import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def show_dashboard():
    st.title("대시보드")
    
    # 예시 데이터 생성
    equipment_data = {
        'equipment_number': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
        'status': ['정상', '점검중', '정상', '고장', '정상'],
        'last_check': [
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=1)
        ]
    }
    
    error_data = {
        'date': pd.date_range(start='2024-01-01', periods=5),
        'error_count': [5, 3, 7, 2, 4]
    }
    
    # 레이아웃 구성
    col1, col2 = st.columns(2)
    
    # 설비 상태 요약
    with col1:
        st.subheader("설비 상태")
        df_equipment = pd.DataFrame(equipment_data)
        
        # 상태별 색상 지정
        status_colors = {
            '정상': 'green',
            '점검중': 'orange',
            '고장': 'red'
        }
        
        # 각 상태별 개수 계산
        status_counts = df_equipment['status'].value_counts()
        
        # 원형 차트
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="설비 상태 분포",
            color=status_counts.index,
            color_discrete_map=status_colors
        )
        st.plotly_chart(fig_status)
        
        # 설비 목록 테이블
        st.dataframe(
            df_equipment,
            column_config={
                "equipment_number": "설비 번호",
                "status": "상태",
                "last_check": st.column_config.DatetimeColumn(
                    "최근 점검일",
                    format="YYYY-MM-DD HH:mm"
                )
            }
        )
    
    # 오류 발생 추이
    with col2:
        st.subheader("오류 발생 추이")
        df_errors = pd.DataFrame(error_data)
        
        # 선 그래프
        fig_errors = px.line(
            df_errors,
            x='date',
            y='error_count',
            title="일별 오류 발생 건수",
            markers=True
        )
        fig_errors.update_layout(
            xaxis_title="날짜",
            yaxis_title="오류 건수"
        )
        st.plotly_chart(fig_errors)
        
        # 통계 정보
        total_errors = df_errors['error_count'].sum()
        avg_errors = df_errors['error_count'].mean()
        
        st.metric(label="총 오류 건수", value=f"{total_errors}건")
        st.metric(label="일평균 오류 건수", value=f"{avg_errors:.1f}건") 