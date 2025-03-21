import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_settings():
    """관리자 설정 페이지를 표시합니다."""
    st.title("관리자 설정")
    
    if st.session_state.user.get('role') != 'admin':
        st.error("관리자 권한이 필요합니다.")
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
        st.subheader("사용자 목록")
        users_data = {
            'email': ['user1@example.com', 'user2@example.com', 'admin@example.com'],
            'role': ['user', 'user', 'admin'],
            'created_at': [
                datetime.now(),
                datetime.now(),
                datetime.now()
            ]
        }
        df_users = pd.DataFrame(users_data)
        st.dataframe(
            df_users,
            column_config={
                "email": "이메일",
                "role": "권한",
                "created_at": st.column_config.DatetimeColumn(
                    "생성일시",
                    format="YYYY-MM-DD HH:mm"
                )
            }
        )
        
        with st.form("user_role_form"):
            st.subheader("사용자 권한 변경")
            email = st.selectbox("사용자 선택", options=df_users['email'].tolist())
            role = st.selectbox("새 권한", options=['user', 'admin'])
            if st.form_submit_button("권한 변경"):
                st.success(f"{email}의 권한이 {role}로 변경되었습니다.")
    
    # 설비 관리
    with tab2:
        st.subheader("설비 목록")
        equipment_data = {
            'equipment_number': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
            'building': ['A동', 'B동', 'A동', 'C동', 'B동'],
            'equipment_type': ['프레스', '컨베이어', '로봇', '프레스', '로봇'],
            'status': ['정상', '점검중', '정상', '고장', '정상']
        }
        df_equipment = pd.DataFrame(equipment_data)
        st.dataframe(
            df_equipment,
            column_config={
                "equipment_number": "설비 번호",
                "building": "건물",
                "equipment_type": "설비 유형",
                "status": "상태"
            }
        )
        
        with st.form("equipment_form"):
            st.subheader("설비 추가")
            new_equipment = st.text_input("설비 번호")
            new_building = st.selectbox("건물", options=['A동', 'B동', 'C동'])
            new_type = st.selectbox("설비 유형", options=['프레스', '컨베이어', '로봇'])
            if st.form_submit_button("설비 추가"):
                if new_equipment:
                    st.success(f"설비 {new_equipment}가 추가되었습니다.")
                else:
                    st.error("설비 번호를 입력해주세요.")
    
    # 오류 코드 관리
    with tab3:
        st.subheader("오류 코드 목록")
        error_codes_data = {
            'error_code': ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005'],
            'description': ['모터 과열', '센서 오류', '전원 불안정', '압력 이상', '통신 오류'],
            'error_type': ['하드웨어', '센서', '전기', '기계', '소프트웨어']
        }
        df_errors = pd.DataFrame(error_codes_data)
        st.dataframe(
            df_errors,
            column_config={
                "error_code": "오류 코드",
                "description": "설명",
                "error_type": "유형"
            }
        )
        
        with st.form("error_code_form"):
            st.subheader("오류 코드 추가")
            new_code = st.text_input("오류 코드")
            new_description = st.text_input("설명")
            new_type = st.selectbox("유형", options=['하드웨어', '센서', '전기', '기계', '소프트웨어'])
            if st.form_submit_button("오류 코드 추가"):
                if new_code and new_description:
                    st.success(f"오류 코드 {new_code}가 추가되었습니다.")
                else:
                    st.error("모든 필드를 입력해주세요.")
    
    # 부품 관리
    with tab4:
        st.subheader("부품 목록")
        parts_data = {
            'part_code': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'part_name': ['베어링', '모터', '센서', '벨트', '기어'],
            'stock': [10, 5, 15, 8, 12]
        }
        df_parts = pd.DataFrame(parts_data)
        st.dataframe(
            df_parts,
            column_config={
                "part_code": "부품 코드",
                "part_name": "부품명",
                "stock": "재고"
            }
        )
        
        with st.form("parts_form"):
            st.subheader("부품 추가")
            new_part_code = st.text_input("부품 코드")
            new_part_name = st.text_input("부품명")
            new_stock = st.number_input("초기 재고", min_value=0)
            if st.form_submit_button("부품 추가"):
                if new_part_code and new_part_name:
                    st.success(f"부품 {new_part_code}가 추가되었습니다.")
                else:
                    st.error("모든 필드를 입력해주세요.") 