import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_settings():
    """관리자 설정 페이지를 표시합니다."""
    st.title("Cài đặt quản trị / 관리자 설정")
    
    if st.session_state.role != 'admin':
        st.error("Yêu cầu quyền quản trị viên / 관리자 권한이 필요합니다.")
        return
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "Quản lý người dùng / 사용자 관리",
        "Quản lý thiết bị / 설비 관리",
        "Quản lý mã lỗi / 오류 코드 관리",
        "Quản lý linh kiện / 부품 관리"
    ])
    
    # 사용자 관리
    with tab1:
        st.subheader("Danh sách người dùng / 사용자 목록")
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
                "email": "Email / 이메일",
                "role": "Quyền hạn / 권한",
                "created_at": st.column_config.DatetimeColumn(
                    "Ngày tạo / 생성일시",
                    format="YYYY-MM-DD HH:mm"
                )
            }
        )
        
        with st.form("user_role_form"):
            st.subheader("Thay đổi quyền hạn người dùng / 사용자 권한 변경")
            email = st.selectbox("Chọn người dùng / 사용자 선택", options=df_users['email'].tolist())
            role = st.selectbox("Quyền hạn mới / 새 권한", options=['user', 'admin'])
            if st.form_submit_button("Thay đổi quyền hạn / 권한 변경"):
                st.success(f"Quyền hạn của {email} đã được thay đổi thành {role} / {email}의 권한이 {role}로 변경되었습니다.")
    
    # 설비 관리
    with tab2:
        st.subheader("Danh sách thiết bị / 설비 목록")
        equipment_data = {
            'equipment_number': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
            'building': ['Tòa nhà A / A동', 'Tòa nhà B / B동', 'Tòa nhà A / A동', 'Tòa nhà C / C동', 'Tòa nhà B / B동'],
            'equipment_type': ['Máy ép / 프레스', 'Băng tải / 컨베이어', 'Robot / 로봇', 'Máy ép / 프레스', 'Robot / 로봇'],
            'status': ['Bình thường / 정상', 'Đang kiểm tra / 점검중', 'Bình thường / 정상', 'Hỏng / 고장', 'Bình thường / 정상']
        }
        df_equipment = pd.DataFrame(equipment_data)
        st.dataframe(
            df_equipment,
            column_config={
                "equipment_number": "Số thiết bị / 설비 번호",
                "building": "Tòa nhà / 건물",
                "equipment_type": "Loại thiết bị / 설비 유형",
                "status": "Trạng thái / 상태"
            }
        )
        
        with st.form("equipment_form"):
            st.subheader("Thêm thiết bị / 설비 추가")
            new_equipment = st.text_input("Số thiết bị / 설비 번호")
            new_building = st.selectbox("Tòa nhà / 건물", options=['Tòa nhà A / A동', 'Tòa nhà B / B동', 'Tòa nhà C / C동'])
            new_type = st.selectbox("Loại thiết bị / 설비 유형", options=['Máy ép / 프레스', 'Băng tải / 컨베이어', 'Robot / 로봇'])
            if st.form_submit_button("Thêm thiết bị / 설비 추가"):
                if new_equipment:
                    st.success(f"Đã thêm thiết bị {new_equipment} / 설비 {new_equipment}가 추가되었습니다.")
                else:
                    st.error("Vui lòng nhập số thiết bị / 설비 번호를 입력해주세요.")
    
    # 오류 코드 관리
    with tab3:
        st.subheader("Danh sách mã lỗi / 오류 코드 목록")
        error_codes_data = {
            'error_code': ['ERR001', 'ERR002', 'ERR003', 'ERR004', 'ERR005'],
            'description': [
                'Động cơ quá nhiệt / 모터 과열', 
                'Lỗi cảm biến / 센서 오류', 
                'Nguồn điện không ổn định / 전원 불안정', 
                'Áp suất bất thường / 압력 이상', 
                'Lỗi giao tiếp / 통신 오류'
            ],
            'error_type': [
                'Phần cứng / 하드웨어', 
                'Cảm biến / 센서', 
                'Điện / 전기', 
                'Cơ khí / 기계', 
                'Phần mềm / 소프트웨어'
            ]
        }
        df_errors = pd.DataFrame(error_codes_data)
        st.dataframe(
            df_errors,
            column_config={
                "error_code": "Mã lỗi / 오류 코드",
                "description": "Mô tả / 설명",
                "error_type": "Loại / 유형"
            }
        )
        
        with st.form("error_code_form"):
            st.subheader("Thêm mã lỗi / 오류 코드 추가")
            new_code = st.text_input("Mã lỗi / 오류 코드")
            new_description = st.text_input("Mô tả / 설명")
            new_type = st.selectbox("Loại / 유형", options=[
                'Phần cứng / 하드웨어', 
                'Cảm biến / 센서', 
                'Điện / 전기', 
                'Cơ khí / 기계', 
                'Phần mềm / 소프트웨어'
            ])
            if st.form_submit_button("Thêm mã lỗi / 오류 코드 추가"):
                if new_code and new_description:
                    st.success(f"Đã thêm mã lỗi {new_code} / 오류 코드 {new_code}가 추가되었습니다.")
                else:
                    st.error("Vui lòng điền vào tất cả các trường / 모든 필드를 입력해주세요.")
    
    # 부품 관리
    with tab4:
        st.subheader("Danh sách linh kiện / 부품 목록")
        parts_data = {
            'part_code': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'part_name': [
                'Vòng bi / 베어링', 
                'Động cơ / 모터', 
                'Cảm biến / 센서', 
                'Dây đai / 벨트', 
                'Bánh răng / 기어'
            ],
            'stock': [10, 5, 15, 8, 12]
        }
        df_parts = pd.DataFrame(parts_data)
        st.dataframe(
            df_parts,
            column_config={
                "part_code": "Mã linh kiện / 부품 코드",
                "part_name": "Tên linh kiện / 부품명",
                "stock": "Tồn kho / 재고"
            }
        )
        
        with st.form("parts_form"):
            st.subheader("Thêm linh kiện / 부품 추가")
            new_part_code = st.text_input("Mã linh kiện / 부품 코드")
            new_part_name = st.text_input("Tên linh kiện / 부품명")
            new_stock = st.number_input("Tồn kho ban đầu / 초기 재고", min_value=0)
            if st.form_submit_button("Thêm linh kiện / 부품 추가"):
                if new_part_code and new_part_name:
                    st.success(f"Đã thêm linh kiện {new_part_code} / 부품 {new_part_code}가 추가되었습니다.")
                else:
                    st.error("Vui lòng điền vào tất cả các trường / 모든 필드를 입력해주세요.") 