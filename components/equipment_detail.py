import streamlit as st
import pandas as pd
from datetime import datetime
from utils.supabase_client import (
    get_equipment_list,
    get_error_history,
    get_parts_replacement
)

def show_equipment_detail():
    """장비 상세 정보를 표시합니다."""
    st.title("설비 상세 정보")
    
    # 설비 목록 로드
    equipment_list = get_equipment_list()
    if not equipment_list:
        st.error("설비 정보를 불러올 수 없습니다.")
        return
    
    # 설비 선택
    df_equipment = pd.DataFrame(equipment_list)
    selected_equipment = st.selectbox(
        "설비 선택",
        df_equipment['equipment_number'].tolist(),
        format_func=lambda x: f"{x} ({df_equipment[df_equipment['equipment_number'] == x]['equipment_type'].iloc[0]})"
    )
    
    if selected_equipment:
        # 선택된 설비 정보 표시
        equipment_info = df_equipment[df_equipment['equipment_number'] == selected_equipment].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("설비 번호", equipment_info['equipment_number'])
        with col2:
            st.metric("설비 유형", equipment_info['equipment_type'])
        with col3:
            st.metric("현재 상태", equipment_info['status'])
        
        # 고장 이력
        st.subheader("고장 이력")
        error_history = get_error_history()
        if error_history:
            df_errors = pd.DataFrame(error_history)
            df_errors = df_errors[df_errors['equipment_number'] == selected_equipment]
            if not df_errors.empty:
                st.dataframe(
                    df_errors,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn(
                            "발생시간",
                            format="YYYY-MM-DD HH:mm"
                        ),
                        "error_code": "에러 코드",
                        "error_detail": "에러 상세",
                        "repair_time": "수리 시간",
                        "repair_method": "수리 방법",
                        "worker": "작업자",
                        "supervisor": "관리자"
                    }
                )
            else:
                st.info("고장 이력이 없습니다.")
        
        # 부품 교체 이력
        st.subheader("부품 교체 이력")
        parts_history = get_parts_replacement()
        if parts_history:
            df_parts = pd.DataFrame(parts_history)
            df_parts = df_parts[df_parts['equipment_number'] == selected_equipment]
            if not df_parts.empty:
                st.dataframe(
                    df_parts,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn(
                            "교체시간",
                            format="YYYY-MM-DD HH:mm"
                        ),
                        "part_code": "부품 코드",
                        "worker": "작업자",
                        "supervisor": "관리자"
                    }
                )
            else:
                st.info("부품 교체 이력이 없습니다.") 