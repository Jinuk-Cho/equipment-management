import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show_data_input():
    """데이터 입력 페이지를 표시합니다."""
    st.title("데이터 입력")
    
    # 예시 데이터 생성
    equipment_list = ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005']
    error_codes = ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005']
    parts_list = ['P001 - 베어링', 'P002 - 모터', 'P003 - 센서', 'P004 - 벨트', 'P005 - 기어']
    
    # 입력 폼
    with st.form("data_input_form"):
        st.subheader("오류 정보 입력")
        
        # 기본 정보
        col1, col2 = st.columns(2)
        with col1:
            equipment = st.selectbox("설비 선택", options=equipment_list)
            error_code = st.selectbox("오류 코드", options=error_codes)
        
        with col2:
            error_datetime = st.date_input("발생 일시", value=datetime.now())
            repair_time = st.number_input("수리 시간 (시간)", min_value=0.0, step=0.5)
        
        # 상세 정보
        error_detail = st.text_area("오류 상세 내용")
        repair_method = st.text_area("수리 방법")
        
        # 부품 교체 정보
        st.subheader("부품 교체 정보")
        replaced_parts = st.multiselect("교체 부품", options=parts_list)
        
        # 작업자 정보
        col3, col4 = st.columns(2)
        with col3:
            worker = st.text_input("작업자")
        with col4:
            supervisor = st.text_input("담당자")
        
        # 제출 버튼
        submitted = st.form_submit_button("저장")
        
        if submitted:
            if not equipment or not error_code or not worker or not supervisor:
                st.error("필수 항목을 모두 입력해주세요.")
            else:
                # 여기에 데이터 저장 로직 추가 예정
                st.success("데이터가 저장되었습니다.")
                st.balloons()
    
    # QR 코드 스캔 기능 (모바일용)
    st.markdown("---")
    st.subheader("QR 코드 스캔")
    st.info("모바일에서 QR 코드를 스캔하면 자동으로 설비 정보가 입력됩니다.") 