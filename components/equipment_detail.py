import streamlit as st
import pandas as pd
import plotly.express as px
from utils.google_sheet import get_sheet_data

def show_equipment_detail():
    """장비 상세 정보를 표시합니다."""
    st.title("장비 상세 조회")
    
    # 구글 시트에서 데이터 가져오기
    if 'credentials' not in st.session_state:
        st.error("Google 계정 인증이 필요합니다.")
        return
    
    # 설비 목록 가져오기
    equipment_list = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "설비목록!A1:D"
    )
    
    # 설비 선택
    selected_equipment = st.selectbox(
        "설비 선택",
        options=equipment_list['설비번호'].tolist(),
        format_func=lambda x: f"{x} ({equipment_list[equipment_list['설비번호'] == x]['건물'].iloc[0]})"
    )
    
    if selected_equipment:
        # 선택된 설비 정보 표시
        equipment_info = equipment_list[equipment_list['설비번호'] == selected_equipment].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("설비 번호", selected_equipment)
        with col2:
            st.metric("건물", equipment_info['건물'])
        with col3:
            st.metric("현재 상태", equipment_info['상태'])
        
        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["오류 이력", "부품 교체 이력", "예방 점검 일정"])
        
        # 오류 이력 탭
        with tab1:
            error_history = get_sheet_data(
                st.session_state['credentials'],
                st.secrets["sheet_id"],
                "오류이력!A1:F"
            )
            
            equipment_errors = error_history[error_history['설비번호'] == selected_equipment]
            if not equipment_errors.empty:
                st.dataframe(equipment_errors, use_container_width=True)
                
                # 오류 발생 추이 차트
                fig = px.line(
                    equipment_errors,
                    x='발생시간',
                    y='지연시간',
                    title="오류 발생 추이"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("오류 이력이 없습니다.")
        
        # 부품 교체 이력 탭
        with tab2:
            parts_history = get_sheet_data(
                st.session_state['credentials'],
                st.secrets["sheet_id"],
                "부품교체!A1:E"
            )
            
            equipment_parts = parts_history[parts_history['설비번호'] == selected_equipment]
            if not equipment_parts.empty:
                st.dataframe(equipment_parts, use_container_width=True)
                
                # 부품별 교체 횟수 차트
                parts_count = equipment_parts['부품명'].value_counts()
                fig = px.bar(
                    x=parts_count.index,
                    y=parts_count.values,
                    title="부품별 교체 횟수"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("부품 교체 이력이 없습니다.")
        
        # 예방 점검 일정 탭
        with tab3:
            maintenance_schedule = get_sheet_data(
                st.session_state['credentials'],
                st.secrets["sheet_id"],
                "예방점검!A1:D"
            )
            
            equipment_maintenance = maintenance_schedule[maintenance_schedule['설비번호'] == selected_equipment]
            if not equipment_maintenance.empty:
                st.dataframe(equipment_maintenance, use_container_width=True)
            else:
                st.info("예정된 예방 점검이 없습니다.") 