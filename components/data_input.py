import streamlit as st
import pandas as pd
from datetime import datetime
from utils.google_sheet import get_sheet_data, append_sheet_data

def show_data_input():
    """데이터 입력 페이지를 표시합니다."""
    st.title("데이터 입력")
    
    if 'credentials' not in st.session_state:
        st.error("Google 계정 인증이 필요합니다.")
        return
    
    # 설비 목록 가져오기
    equipment_list = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "설비목록!A1:D"
    )
    
    # 오류 코드 목록 가져오기
    error_codes = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "오류코드!A1:C"
    )
    
    # 부품 목록 가져오기
    parts_list = get_sheet_data(
        st.session_state['credentials'],
        st.secrets["sheet_id"],
        "부품목록!A1:C"
    )
    
    # 입력 폼
    with st.form("data_input_form"):
        st.subheader("작업 정보 입력")
        
        # 날짜 및 시간 (자동)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.text(f"입력 시간: {current_time}")
        
        # 설비 선택
        selected_equipment = st.selectbox(
            "설비 선택",
            options=equipment_list['설비번호'].tolist(),
            format_func=lambda x: f"{x} ({equipment_list[equipment_list['설비번호'] == x]['건물'].iloc[0]})"
        )
        
        # 오류 코드 선택
        selected_error = st.selectbox(
            "오류 코드",
            options=error_codes['코드'].tolist(),
            format_func=lambda x: f"{x} - {error_codes[error_codes['코드'] == x]['설명'].iloc[0]}"
        )
        
        # 상세 내용
        error_detail = st.text_area("상세 내용")
        
        # 작업 정보
        col1, col2 = st.columns(2)
        with col1:
            repair_time = st.number_input("수리 시간 (분)", min_value=0)
        with col2:
            repair_method = st.text_input("수리 방법")
        
        # 교체 부품 선택 (다중 선택)
        replaced_parts = st.multiselect(
            "교체 부품",
            options=parts_list['부품코드'].tolist(),
            format_func=lambda x: f"{x} - {parts_list[parts_list['부품코드'] == x]['부품명'].iloc[0]}"
        )
        
        # 작업자 정보
        col3, col4 = st.columns(2)
        with col3:
            worker = st.text_input("작업자")
        with col4:
            supervisor = st.text_input("확인자")
        
        # 제출 버튼
        submitted = st.form_submit_button("저장")
        
        if submitted:
            # 오류 이력에 추가
            error_data = [
                [current_time, selected_equipment, selected_error, error_detail, 
                 repair_time, repair_method, worker, supervisor]
            ]
            
            error_result = append_sheet_data(
                st.session_state['credentials'],
                st.secrets["sheet_id"],
                "오류이력!A1",
                error_data
            )
            
            # 부품 교체 이력에 추가
            if replaced_parts:
                parts_data = [
                    [current_time, selected_equipment, part, worker, supervisor]
                    for part in replaced_parts
                ]
                
                parts_result = append_sheet_data(
                    st.session_state['credentials'],
                    st.secrets["sheet_id"],
                    "부품교체!A1",
                    parts_data
                )
            
            if error_result:
                st.success("데이터가 성공적으로 저장되었습니다.")
            else:
                st.error("데이터 저장 중 오류가 발생했습니다.")
    
    # QR 코드 스캔 기능 (모바일용)
    st.markdown("---")
    st.subheader("QR 코드 스캔")
    st.info("모바일에서 QR 코드를 스캔하면 자동으로 설비 정보가 입력됩니다.") 