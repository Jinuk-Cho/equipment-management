import streamlit as st
import pandas as pd
import plotly.express as px
from utils.google_sheet import get_sheet_data, get_equipment_status

def show_dashboard():
    """실시간 대시보드를 표시합니다."""
    st.title("실시간 설비 상태 대시보드")
    
    # 설비 상태 데이터 가져오기
    if 'credentials' in st.session_state:
        equipment_data = get_sheet_data(
            st.session_state['credentials'],
            st.secrets["sheet_id"],
            "설비상태!A1:E"
        )
    else:
        st.error("Google 계정 인증이 필요합니다.")
        return
    
    # 상단 KPI 지표
    col1, col2, col3, col4 = st.columns(4)
    
    total_equipment = len(equipment_data)
    running_equipment = len(equipment_data[equipment_data['상태'] == '가동중'])
    faulty_equipment = len(equipment_data[equipment_data['상태'] == '고장'])
    maintenance_equipment = len(equipment_data[equipment_data['상태'] == '점검중'])
    
    with col1:
        st.metric("총 설비 수", f"{total_equipment}대")
    with col2:
        st.metric("가동 설비", f"{running_equipment}대")
    with col3:
        st.metric("고장 설비", f"{faulty_equipment}대")
    with col4:
        st.metric("점검 중", f"{maintenance_equipment}대")
    
    # 두 개의 행으로 나누기
    row1_col1, row1_col2 = st.columns(2)
    
    # 좌측 상단: 설비 상태 원형 차트
    with row1_col1:
        st.subheader("설비 상태 현황")
        status_counts = equipment_data['상태'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 우측 상단: 구역별 설비 현황
    with row1_col2:
        st.subheader("구역별 설비 현황")
        building_status = pd.crosstab(equipment_data['건물'], equipment_data['상태'])
        fig = px.bar(
            building_status,
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 하단: 고장 설비 목록
    st.subheader("현재 고장 설비 목록")
    faulty_equipment = equipment_data[equipment_data['상태'] == '고장']
    if not faulty_equipment.empty:
        st.dataframe(
            faulty_equipment[['설비번호', '건물', '오류코드', '발생시간', '담당자']],
            use_container_width=True
        )
    else:
        st.info("현재 고장난 설비가 없습니다.")
    
    # 필터 및 검색
    st.sidebar.subheader("필터 옵션")
    selected_building = st.sidebar.multiselect(
        "건물 선택",
        options=equipment_data['건물'].unique()
    )
    
    search_equipment = st.sidebar.text_input("설비 번호 검색")
    
    if selected_building or search_equipment:
        filtered_data = equipment_data.copy()
        
        if selected_building:
            filtered_data = filtered_data[filtered_data['건물'].isin(selected_building)]
        
        if search_equipment:
            filtered_data = filtered_data[filtered_data['설비번호'].astype(str).str.contains(search_equipment)]
        
        st.subheader("필터링된 설비 목록")
        st.dataframe(filtered_data, use_container_width=True) 