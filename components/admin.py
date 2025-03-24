import streamlit as st
import pandas as pd
from datetime import datetime
from components.language import get_text

# 관리자 설정 페이지 텍스트
ADMIN_TEXTS = {
    "admin_settings": {
        "ko": "관리자 설정",
        "vi": "Cài đặt quản trị"
    },
    "admin_required": {
        "ko": "관리자 권한이 필요합니다.",
        "vi": "Yêu cầu quyền quản trị viên"
    },
    "user_management": {
        "ko": "사용자 관리",
        "vi": "Quản lý người dùng"
    },
    "equipment_management": {
        "ko": "설비 관리",
        "vi": "Quản lý thiết bị"
    },
    "error_code_management": {
        "ko": "오류 코드 관리",
        "vi": "Quản lý mã lỗi"
    },
    "parts_management": {
        "ko": "부품 관리",
        "vi": "Quản lý linh kiện"
    },
    "user_list": {
        "ko": "사용자 목록",
        "vi": "Danh sách người dùng"
    },
    "email": {
        "ko": "이메일",
        "vi": "Email"
    },
    "role": {
        "ko": "권한",
        "vi": "Quyền hạn"
    },
    "creation_date": {
        "ko": "생성일시",
        "vi": "Ngày tạo"
    },
    "change_user_role": {
        "ko": "사용자 권한 변경",
        "vi": "Thay đổi quyền hạn người dùng"
    },
    "select_user": {
        "ko": "사용자 선택",
        "vi": "Chọn người dùng"
    },
    "new_role": {
        "ko": "새 권한",
        "vi": "Quyền hạn mới"
    },
    "change_role": {
        "ko": "권한 변경",
        "vi": "Thay đổi quyền hạn"
    },
    "role_changed": {
        "ko": "의 권한이 로 변경되었습니다.",
        "vi": "đã được thay đổi thành"
    },
    "equipment_list": {
        "ko": "설비 목록",
        "vi": "Danh sách thiết bị"
    },
    "equipment_number": {
        "ko": "설비 번호",
        "vi": "Số thiết bị"
    },
    "building": {
        "ko": "건물",
        "vi": "Tòa nhà"
    },
    "equipment_type": {
        "ko": "설비 유형",
        "vi": "Loại thiết bị"
    },
    "status": {
        "ko": "상태",
        "vi": "Trạng thái"
    },
    "add_equipment": {
        "ko": "설비 추가",
        "vi": "Thêm thiết bị"
    },
    "equipment_added": {
        "ko": "설비 가 추가되었습니다.",
        "vi": "Đã thêm thiết bị"
    },
    "enter_equipment_number": {
        "ko": "설비 번호를 입력해주세요.",
        "vi": "Vui lòng nhập số thiết bị"
    },
    "error_code_list": {
        "ko": "오류 코드 목록",
        "vi": "Danh sách mã lỗi"
    },
    "error_code": {
        "ko": "오류 코드",
        "vi": "Mã lỗi"
    },
    "description": {
        "ko": "설명",
        "vi": "Mô tả"
    },
    "error_type": {
        "ko": "유형",
        "vi": "Loại"
    },
    "add_error_code": {
        "ko": "오류 코드 추가",
        "vi": "Thêm mã lỗi"
    },
    "error_code_added": {
        "ko": "오류 코드 가 추가되었습니다.",
        "vi": "Đã thêm mã lỗi"
    },
    "fill_all_fields": {
        "ko": "모든 필드를 입력해주세요.",
        "vi": "Vui lòng điền vào tất cả các trường"
    },
    "parts_list": {
        "ko": "부품 목록",
        "vi": "Danh sách linh kiện"
    },
    "part_code": {
        "ko": "부품 코드",
        "vi": "Mã linh kiện"
    },
    "part_name": {
        "ko": "부품명",
        "vi": "Tên linh kiện"
    },
    "stock": {
        "ko": "재고",
        "vi": "Tồn kho"
    },
    "add_part": {
        "ko": "부품 추가",
        "vi": "Thêm linh kiện"
    },
    "initial_stock": {
        "ko": "초기 재고",
        "vi": "Tồn kho ban đầu"
    },
    "part_added": {
        "ko": "부품 가 추가되었습니다.",
        "vi": "Đã thêm linh kiện"
    }
}

def get_admin_text(key, lang):
    """관리자 설정 페이지 전용 텍스트를 가져옵니다."""
    if key in ADMIN_TEXTS:
        return ADMIN_TEXTS[key].get(lang, ADMIN_TEXTS[key]['ko'])
    return f"[{key}]"

def show_admin_settings(lang='ko'):
    """관리자 설정 페이지를 표시합니다."""
    st.title(get_admin_text("admin_settings", lang))
    
    if st.session_state.role != 'admin':
        st.error(get_admin_text("admin_required", lang))
        return
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        get_admin_text("user_management", lang),
        get_admin_text("equipment_management", lang),
        get_admin_text("error_code_management", lang),
        get_admin_text("parts_management", lang)
    ])
    
    # 사용자 관리
    with tab1:
        st.subheader(get_admin_text("user_list", lang))
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
                "email": get_admin_text("email", lang),
                "role": get_admin_text("role", lang),
                "created_at": st.column_config.DatetimeColumn(
                    get_admin_text("creation_date", lang),
                    format="YYYY-MM-DD HH:mm"
                )
            }
        )
        
        with st.form("user_role_form"):
            st.subheader(get_admin_text("change_user_role", lang))
            email = st.selectbox(get_admin_text("select_user", lang), options=df_users['email'].tolist())
            role = st.selectbox(get_admin_text("new_role", lang), options=['user', 'admin'])
            if st.form_submit_button(get_admin_text("change_role", lang)):
                st.success(f"{email} {get_admin_text('role_changed', lang)} {role}")
    
    # 설비 관리
    with tab2:
        st.subheader(get_admin_text("equipment_list", lang))
        
        # 건물 및 설비 유형 설정
        buildings = {
            'ko': ['A동', 'B동', 'C동'],
            'vi': ['Tòa nhà A', 'Tòa nhà B', 'Tòa nhà C']
        }
        
        equipment_types = {
            'ko': ['프레스', '컨베이어', '로봇'],
            'vi': ['Máy ép', 'Băng tải', 'Robot']
        }
        
        status_types = {
            'ko': ['정상', '점검중', '고장'],
            'vi': ['Bình thường', 'Đang kiểm tra', 'Hỏng']
        }
        
        # 예시 데이터 생성
        equipment_data = []
        for i in range(5):
            idx = i % 3
            equipment_data.append({
                'equipment_number': f'EQ00{i+1}',
                'building': buildings[lang][idx],
                'equipment_type': equipment_types[lang][i % len(equipment_types[lang])],
                'status': status_types[lang][i % len(status_types[lang])]
            })
        
        df_equipment = pd.DataFrame(equipment_data)
        st.dataframe(
            df_equipment,
            column_config={
                "equipment_number": get_admin_text("equipment_number", lang),
                "building": get_admin_text("building", lang),
                "equipment_type": get_admin_text("equipment_type", lang),
                "status": get_admin_text("status", lang)
            }
        )
        
        with st.form("equipment_form"):
            st.subheader(get_admin_text("add_equipment", lang))
            new_equipment = st.text_input(get_admin_text("equipment_number", lang))
            new_building = st.selectbox(get_admin_text("building", lang), options=buildings[lang])
            new_type = st.selectbox(get_admin_text("equipment_type", lang), options=equipment_types[lang])
            if st.form_submit_button(get_admin_text("add_equipment", lang)):
                if new_equipment:
                    st.success(f"{get_admin_text('equipment_added', lang)} {new_equipment}")
                else:
                    st.error(get_admin_text("enter_equipment_number", lang))
    
    # 오류 코드 관리
    with tab3:
        st.subheader(get_admin_text("error_code_list", lang))
        
        # 오류 유형 설정
        error_types = {
            'ko': ['하드웨어', '센서', '전기', '기계', '소프트웨어'],
            'vi': ['Phần cứng', 'Cảm biến', 'Điện', 'Cơ khí', 'Phần mềm']
        }
        
        # 설명 설정
        descriptions = {
            'ko': ['모터 과열', '센서 오류', '전원 불안정', '압력 이상', '통신 오류'],
            'vi': ['Động cơ quá nhiệt', 'Lỗi cảm biến', 'Nguồn điện không ổn định', 'Áp suất bất thường', 'Lỗi giao tiếp']
        }
        
        error_codes_data = []
        for i in range(5):
            error_codes_data.append({
                'error_code': f'ERR00{i+1}',
                'description': descriptions[lang][i],
                'error_type': error_types[lang][i]
            })
        
        df_errors = pd.DataFrame(error_codes_data)
        st.dataframe(
            df_errors,
            column_config={
                "error_code": get_admin_text("error_code", lang),
                "description": get_admin_text("description", lang),
                "error_type": get_admin_text("error_type", lang)
            }
        )
        
        with st.form("error_code_form"):
            st.subheader(get_admin_text("add_error_code", lang))
            new_code = st.text_input(get_admin_text("error_code", lang))
            new_description = st.text_input(get_admin_text("description", lang))
            new_type = st.selectbox(get_admin_text("error_type", lang), options=error_types[lang])
            if st.form_submit_button(get_admin_text("add_error_code", lang)):
                if new_code and new_description:
                    st.success(f"{get_admin_text('error_code_added', lang)} {new_code}")
                else:
                    st.error(get_admin_text("fill_all_fields", lang))
    
    # 부품 관리
    with tab4:
        st.subheader(get_admin_text("parts_list", lang))
        
        # 부품명 설정
        part_names = {
            'ko': ['베어링', '모터', '센서', '벨트', '기어'],
            'vi': ['Vòng bi', 'Động cơ', 'Cảm biến', 'Dây đai', 'Bánh răng']
        }
        
        parts_data = []
        for i in range(5):
            parts_data.append({
                'part_code': f'P00{i+1}',
                'part_name': part_names[lang][i],
                'stock': [10, 5, 15, 8, 12][i]
            })
        
        df_parts = pd.DataFrame(parts_data)
        st.dataframe(
            df_parts,
            column_config={
                "part_code": get_admin_text("part_code", lang),
                "part_name": get_admin_text("part_name", lang),
                "stock": get_admin_text("stock", lang)
            }
        )
        
        with st.form("parts_form"):
            st.subheader(get_admin_text("add_part", lang))
            new_part_code = st.text_input(get_admin_text("part_code", lang))
            new_part_name = st.text_input(get_admin_text("part_name", lang))
            new_stock = st.number_input(get_admin_text("initial_stock", lang), min_value=0)
            if st.form_submit_button(get_admin_text("add_part", lang)):
                if new_part_code and new_part_name:
                    st.success(f"{get_admin_text('part_added', lang)} {new_part_code}")
                else:
                    st.error(get_admin_text("fill_all_fields", lang)) 