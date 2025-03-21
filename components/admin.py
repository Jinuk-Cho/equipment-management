import streamlit as st
import pandas as pd
from utils.auth import create_user, update_user_role, delete_user, load_users
from utils.google_sheet import get_sheet_data, append_sheet_data, update_sheet_data

def show_admin_settings():
    """관리자 설정 페이지를 표시합니다."""
    st.title("관리자 설정")
    
    if 'credentials' not in st.session_state:
        st.error("Google 계정 인증이 필요합니다.")
        return
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "사용자 관리",
        "설비 관리",
        "오류 코드 관리",
        "부품 관리"
    ])
    
    # 사용자 관리
    with tab1:
        st.subheader("사용자 관리")
        
        # 현재 사용자 목록
        users = load_users()
        users_df = pd.DataFrame([
            {"사용자명": username, "권한": data["role"]}
            for username, data in users.items()
        ])
        
        if not users_df.empty:
            st.dataframe(users_df, use_container_width=True)
        
        # 새 사용자 추가
        st.subheader("새 사용자 추가")
        with st.form("new_user_form"):
            new_username = st.text_input("사용자명")
            new_password = st.text_input("비밀번호", type="password")
            new_role = st.selectbox("권한", ["user", "leader", "admin"])
            
            if st.form_submit_button("추가"):
                if create_user(new_username, new_password, new_role):
                    st.success("사용자가 추가되었습니다.")
                    st.rerun()
                else:
                    st.error("이미 존재하는 사용자명입니다.")
        
        # 사용자 권한 변경
        st.subheader("사용자 권한 변경")
        with st.form("update_user_form"):
            update_username = st.selectbox("사용자 선택", list(users.keys()))
            update_role = st.selectbox("새 권한", ["user", "leader", "admin"])
            
            if st.form_submit_button("변경"):
                if update_user_role(update_username, update_role):
                    st.success("권한이 변경되었습니다.")
                    st.rerun()
                else:
                    st.error("권한 변경에 실패했습니다.")
        
        # 사용자 삭제
        st.subheader("사용자 삭제")
        with st.form("delete_user_form"):
            delete_username = st.selectbox("삭제할 사용자", list(users.keys()))
            
            if st.form_submit_button("삭제"):
                if delete_user(delete_username):
                    st.success("사용자가 삭제되었습니다.")
                    st.rerun()
                else:
                    st.error("사용자 삭제에 실패했습니다.")
    
    # 설비 관리
    with tab2:
        st.subheader("설비 관리")
        
        # 현재 설비 목록
        equipment_list = get_sheet_data(
            st.session_state['credentials'],
            st.secrets["sheet_id"],
            "설비목록!A1:D"
        )
        
        if not equipment_list.empty:
            st.dataframe(equipment_list, use_container_width=True)
        
        # 새 설비 추가
        st.subheader("새 설비 추가")
        with st.form("new_equipment_form"):
            new_equipment_id = st.text_input("설비 번호")
            new_equipment_building = st.selectbox("건물", ["A동", "B동"])
            new_equipment_type = st.text_input("설비 유형")
            
            if st.form_submit_button("추가"):
                new_data = [[new_equipment_id, new_equipment_building, new_equipment_type, "정상"]]
                if append_sheet_data(
                    st.session_state['credentials'],
                    st.secrets["sheet_id"],
                    "설비목록!A1",
                    new_data
                ):
                    st.success("설비가 추가되었습니다.")
                    st.rerun()
                else:
                    st.error("설비 추가에 실패했습니다.")
    
    # 오류 코드 관리
    with tab3:
        st.subheader("오류 코드 관리")
        
        # 현재 오류 코드 목록
        error_codes = get_sheet_data(
            st.session_state['credentials'],
            st.secrets["sheet_id"],
            "오류코드!A1:C"
        )
        
        if not error_codes.empty:
            st.dataframe(error_codes, use_container_width=True)
        
        # 새 오류 코드 추가
        st.subheader("새 오류 코드 추가")
        with st.form("new_error_code_form"):
            new_error_code = st.text_input("오류 코드")
            new_error_desc = st.text_input("설명")
            new_error_type = st.selectbox("유형", ["하드웨어", "소프트웨어", "기타"])
            
            if st.form_submit_button("추가"):
                new_data = [[new_error_code, new_error_desc, new_error_type]]
                if append_sheet_data(
                    st.session_state['credentials'],
                    st.secrets["sheet_id"],
                    "오류코드!A1",
                    new_data
                ):
                    st.success("오류 코드가 추가되었습니다.")
                    st.rerun()
                else:
                    st.error("오류 코드 추가에 실패했습니다.")
    
    # 부품 관리
    with tab4:
        st.subheader("부품 관리")
        
        # 현재 부품 목록
        parts_list = get_sheet_data(
            st.session_state['credentials'],
            st.secrets["sheet_id"],
            "부품목록!A1:C"
        )
        
        if not parts_list.empty:
            st.dataframe(parts_list, use_container_width=True)
        
        # 새 부품 추가
        st.subheader("새 부품 추가")
        with st.form("new_part_form"):
            new_part_code = st.text_input("부품 코드")
            new_part_name = st.text_input("부품명")
            new_part_stock = st.number_input("재고", min_value=0)
            
            if st.form_submit_button("추가"):
                new_data = [[new_part_code, new_part_name, new_part_stock]]
                if append_sheet_data(
                    st.session_state['credentials'],
                    st.secrets["sheet_id"],
                    "부품목록!A1",
                    new_data
                ):
                    st.success("부품이 추가되었습니다.")
                    st.rerun()
                else:
                    st.error("부품 추가에 실패했습니다.") 