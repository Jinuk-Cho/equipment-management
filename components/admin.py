import streamlit as st
import pandas as pd
from datetime import datetime
from components.language import get_text, get_admin_text
from utils.supabase_client import get_supabase, fetch_data, sign_up_user, update_data, delete_data, insert_data, get_equipment_serials, add_equipment_serial, update_equipment_serial, delete_equipment_serial, bulk_upload_equipment_serials
import io
import csv

# Supabase 클라이언트 가져오기
supabase = get_supabase()

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
    },
    "add_user": {
        "ko": "사용자 추가",
        "vi": "Thêm người dùng"
    },
    "name": {
        "ko": "이름",
        "vi": "Tên"
    },
    "department": {
        "ko": "부서",
        "vi": "Phòng ban"
    },
    "phone": {
        "ko": "전화번호",
        "vi": "Số điện thoại"
    },
    "password": {
        "ko": "비밀번호",
        "vi": "Mật khẩu"
    },
    "confirm_password": {
        "ko": "비밀번호 확인",
        "vi": "Xác nhận mật khẩu"
    },
    "user_added": {
        "ko": "사용자가 추가되었습니다.",
        "vi": "Người dùng đã được thêm."
    },
    "user_deleted": {
        "ko": "사용자가 삭제되었습니다.",
        "vi": "Người dùng đã bị xóa."
    },
    "delete_user": {
        "ko": "사용자 삭제",
        "vi": "Xóa người dùng"
    },
    "delete_confirm": {
        "ko": "정말 삭제하시겠습니까?",
        "vi": "Bạn có chắc chắn muốn xóa không?"
    },
    "last_login": {
        "ko": "마지막 로그인",
        "vi": "Đăng nhập lần cuối"
    },
    "action": {
        "ko": "작업",
        "vi": "Thao tác"
    },
    "equipment_serial_management": {
        "ko": "설비-시리얼 관리",
        "vi": "Quản lý thiết bị-serial"
    },
    "serial_number": {
        "ko": "시리얼 번호",
        "vi": "Số serial"
    },
    "add_equipment_serial": {
        "ko": "설비-시리얼 추가",
        "vi": "Thêm thiết bị-serial"
    },
    "update_equipment_serial": {
        "ko": "설비-시리얼 수정",
        "vi": "Cập nhật thiết bị-serial"
    },
    "delete_equipment_serial": {
        "ko": "설비-시리얼 삭제",
        "vi": "Xóa thiết bị-serial"
    },
    "bulk_upload": {
        "ko": "일괄 업로드",
        "vi": "Tải lên hàng loạt"
    },
    "upload_csv": {
        "ko": "CSV 파일 업로드",
        "vi": "Tải lên tệp CSV"
    },
    "csv_format": {
        "ko": "CSV 형식은 'equipment_number,serial_number'입니다. 헤더 포함.",
        "vi": "Định dạng CSV là 'equipment_number,serial_number'. Bao gồm tiêu đề."
    },
    "upload_success": {
        "ko": "업로드 성공",
        "vi": "Tải lên thành công"
    },
    "upload_error": {
        "ko": "업로드 오류",
        "vi": "Lỗi tải lên"
    },
    "add_success": {
        "ko": "추가 성공",
        "vi": "Thêm thành công"
    },
    "update_success": {
        "ko": "수정 성공",
        "vi": "Cập nhật thành công"
    },
    "delete_success": {
        "ko": "삭제 성공",
        "vi": "Xóa thành công"
    },
    "existing_equipment": {
        "ko": "이미 존재하는 설비 번호입니다.",
        "vi": "Số thiết bị đã tồn tại."
    },
    "confirm_delete": {
        "ko": "정말 삭제하시겠습니까?",
        "vi": "Bạn có chắc chắn muốn xóa không?"
    },
    "download_template": {
        "ko": "템플릿 다운로드",
        "vi": "Tải xuống mẫu"
    },
    "template_info": {
        "ko": "CSV 템플릿을 다운로드하여 설비 번호와 시리얼 번호를 작성한 후 업로드하세요.",
        "vi": "Tải xuống mẫu CSV, điền số thiết bị và số serial, sau đó tải lên."
    }
}

def get_admin_text(key, lang):
    """관리자 설정 페이지 전용 텍스트를 가져옵니다."""
    if key in ADMIN_TEXTS:
        return ADMIN_TEXTS[key].get(lang, ADMIN_TEXTS[key]['ko'])
    return f"[{key}]"

# 사용자 목록 가져오기
def get_users():
    if not supabase:
        return []
    
    try:
        # Supabase의 users 테이블에서 사용자 정보 가져오기
        response = supabase.table('users').select('*').execute()
        return response.data
    except Exception as e:
        st.error(f"사용자 데이터 조회 실패: {str(e)}")
        return []

# 사용자 추가
def add_user(name, email, password, department, phone, role="user"):
    if not supabase:
        return False
    
    try:
        # 1. Supabase Auth로 사용자 등록
        user = sign_up_user(email, password, role)
        if user:
            # 2. 사용자 메타데이터 추가 정보를 users 테이블에 저장
            user_data = {
                'id': user.id,
                'email': email,
                'name': name,
                'role': role,
                'department': department,
                'phone': phone,
                'created_at': datetime.now().isoformat(),
                'last_login': None
            }
            insert_data('users', user_data)
            return True
        return False
    except Exception as e:
        st.error(f"사용자 추가 실패: {str(e)}")
        return False

# 사용자 권한 변경
def change_user_role(user_id, new_role):
    if not supabase:
        return False
    
    try:
        # 사용자 권한 변경
        update_data('users', {'role': new_role}, 'id', user_id)
        
        # Auth 사용자 메타데이터 업데이트
        supabase.auth.admin.update_user_by_id(user_id, {
            "user_metadata": {"role": new_role}
        })
        return True
    except Exception as e:
        st.error(f"사용자 권한 변경 실패: {str(e)}")
        return False

# 사용자 삭제
def delete_user(user_id):
    if not supabase:
        return False
    
    try:
        # 1. 사용자 테이블에서 삭제
        delete_data('users', 'id', user_id)
        
        # 2. Auth에서 사용자 삭제
        supabase.auth.admin.delete_user(user_id)
        return True
    except Exception as e:
        st.error(f"사용자 삭제 실패: {str(e)}")
        return False

def show_admin_settings(lang='ko'):
    """관리자 설정 페이지를 표시합니다."""
    st.title(get_admin_text("admin_settings", lang))
    
    if st.session_state.role != 'admin':
        st.error(get_admin_text("admin_required", lang))
        return
    
    # 관리 탭
    tabs = st.tabs([
        get_admin_text("user_management", lang),
        get_admin_text("equipment_management", lang),
        get_admin_text("equipment_serial_management", lang),
        get_admin_text("error_code_management", lang),
        get_admin_text("parts_management", lang)
    ])
    
    # 사용자 관리 탭
    with tabs[0]:
        show_user_management(lang)
        
    # 설비 관리 탭
    with tabs[1]:
        show_equipment_management(lang)
        
    # 설비-시리얼 관리 탭
    with tabs[2]:
        show_equipment_serial_management(lang)
        
    # 오류 코드 관리 탭
    with tabs[3]:
        show_error_code_management(lang)
        
    # 부품 관리 탭
    with tabs[4]:
        show_parts_management(lang)

# 사용자 관리 탭 표시
def show_user_management(lang):
    st.subheader(get_admin_text("user_list", lang))
    
    # 사용자 목록 조회
    users = get_users()
    
    if users:
        # 데이터프레임 생성
        df_users = pd.DataFrame(users)
        
        # 액션 컬럼 추가를 위한 빈 열 추가
        df_users['action'] = ''
        
        # 데이터프레임 표시
        edited_df = st.data_editor(
            df_users,
            column_config={
                "id": st.column_config.TextColumn(
                    "ID",
                    width="small",
                    required=True
                ),
                "email": st.column_config.TextColumn(
                    get_admin_text("email", lang),
                    width="medium",
                    required=True
                ),
                "name": st.column_config.TextColumn(
                    get_admin_text("name", lang),
                    width="medium",
                    required=True
                ),
                "role": st.column_config.SelectboxColumn(
                    get_admin_text("role", lang),
                    width="small",
                    options=["admin", "user"],
                    required=True
                ),
                "department": st.column_config.TextColumn(
                    get_admin_text("department", lang),
                    width="medium"
                ),
                "phone": st.column_config.TextColumn(
                    get_admin_text("phone", lang),
                    width="medium"
                ),
                "created_at": st.column_config.DatetimeColumn(
                    get_admin_text("creation_date", lang),
                    format="YYYY-MM-DD HH:mm",
                    width="medium"
                ),
                "last_login": st.column_config.DatetimeColumn(
                    get_admin_text("last_login", lang),
                    format="YYYY-MM-DD HH:mm",
                    width="medium"
                ),
                "action": st.column_config.Column(
                    get_admin_text("action", lang),
                    width="small",
                    disabled=True
                )
            },
            hide_index=True,
            use_container_width=True,
            disabled=["id", "email", "created_at", "last_login", "action"],
            key="user_table"
        )

        # 변경사항 감지 및 업데이트
        if st.session_state.get('user_table', None) is not None:
            for idx, row in edited_df.iterrows():
                if row['role'] != users[idx]['role']:
                    if change_user_role(row['id'], row['role']):
                        st.success(f"{row['name']} {get_admin_text('role_changed', lang)} {row['role']}")
        
        # 사용자 선택 삭제
        cols = st.columns([3, 1])
        with cols[0]:
            selected_user = st.selectbox(
                get_admin_text("select_user", lang),
                options=[user['email'] for user in users],
                key="delete_user_select"
            )
        with cols[1]:
            if st.button(get_admin_text("delete_user", lang), key="delete_user_button", type="primary"):
                if selected_user:
                    user_id = None
                    for user in users:
                        if user['email'] == selected_user:
                            user_id = user['id']
                            break
                    
                    if user_id:
                        if delete_user(user_id):
                            st.success(get_admin_text("user_deleted", lang))
                            st.rerun()
    else:
        st.info("사용자가 없습니다.")
    
    # 사용자 추가 폼
    with st.form("add_user_form"):
        st.subheader(get_admin_text("add_user", lang))
        
        user_name = st.text_input(get_admin_text("name", lang))
        user_email = st.text_input(get_admin_text("email", lang))
        user_dept = st.text_input(get_admin_text("department", lang))
        user_phone = st.text_input(get_admin_text("phone", lang))
        user_role = st.selectbox(
            get_admin_text("role", lang),
            options=["user", "admin"]
        )
        user_password = st.text_input(get_admin_text("password", lang), type="password")
        user_password_confirm = st.text_input(get_admin_text("confirm_password", lang), type="password")
        
        if st.form_submit_button(get_admin_text("add_user", lang)):
            if not user_name or not user_email or not user_password or not user_password_confirm:
                st.error(get_admin_text("fill_all_fields", lang))
            elif user_password != user_password_confirm:
                st.error(get_text("password_mismatch", lang))
            else:
                if add_user(user_name, user_email, user_password, user_dept, user_phone, user_role):
                    st.success(get_admin_text("user_added", lang))
                    st.rerun()

# 설비 관리 탭 표시
def show_equipment_management(lang):
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
    
    # 설비 추가 폼
    with st.form("add_equipment_form"):
        st.subheader(get_admin_text("add_equipment", lang))
        
        cols = st.columns(2)
        with cols[0]:
            equipment_number = st.text_input(get_admin_text("equipment_number", lang))
            building = st.selectbox(
                get_admin_text("building", lang),
                options=buildings[lang]
            )
        
        with cols[1]:
            equipment_type = st.selectbox(
                get_admin_text("equipment_type", lang),
                options=equipment_types[lang]
            )
            status = st.selectbox(
                get_admin_text("status", lang),
                options=status_types[lang]
            )
        
        if st.form_submit_button(get_admin_text("add_equipment", lang)):
            if not equipment_number:
                st.error(get_admin_text("enter_equipment_number", lang))
            else:
                st.success(f"'{equipment_number}' {get_admin_text('equipment_added', lang)}")
                st.rerun()

# 오류 코드 관리 탭 표시
def show_error_code_management(lang):
    st.subheader(get_admin_text("error_code_list", lang))
    
    # 예시 데이터
    error_code_data = [
        {"error_code": "E001", "description": "모터 과열", "error_type": "모터"},
        {"error_code": "E002", "description": "센서 고장", "error_type": "센서"},
        {"error_code": "E003", "description": "전원 문제", "error_type": "전기"},
        {"error_code": "E004", "description": "제어기 오류", "error_type": "제어"},
        {"error_code": "E005", "description": "기계적 고장", "error_type": "기계"}
    ]
    
    df_error_codes = pd.DataFrame(error_code_data)
    st.dataframe(
        df_error_codes,
        column_config={
            "error_code": get_admin_text("error_code", lang),
            "description": get_admin_text("description", lang),
            "error_type": get_admin_text("error_type", lang)
        }
    )
    
    # 오류 코드 추가 폼
    with st.form("add_error_code_form"):
        st.subheader(get_admin_text("add_error_code", lang))
        
        cols = st.columns(3)
        with cols[0]:
            error_code = st.text_input(get_admin_text("error_code", lang))
        
        with cols[1]:
            error_type = st.text_input(get_admin_text("error_type", lang))
        
        with cols[2]:
            description = st.text_input(get_admin_text("description", lang))
        
        if st.form_submit_button(get_admin_text("add_error_code", lang)):
            if not error_code or not error_type or not description:
                st.error(get_admin_text("fill_all_fields", lang))
            else:
                st.success(f"'{error_code}' {get_admin_text('error_code_added', lang)}")
                st.rerun()

# 부품 관리 탭 표시
def show_parts_management(lang):
    st.subheader(get_admin_text("parts_list", lang))
    
    # 예시 데이터
    parts_data = [
        {"part_code": "P001", "part_name": "모터", "stock": 10},
        {"part_code": "P002", "part_name": "센서", "stock": 15},
        {"part_code": "P003", "part_name": "전원 모듈", "stock": 8},
        {"part_code": "P004", "part_name": "제어기", "stock": 5},
        {"part_code": "P005", "part_name": "베어링", "stock": 20}
    ]
    
    df_parts = pd.DataFrame(parts_data)
    st.dataframe(
        df_parts,
        column_config={
            "part_code": get_admin_text("part_code", lang),
            "part_name": get_admin_text("part_name", lang),
            "stock": st.column_config.NumberColumn(
                get_admin_text("stock", lang),
                format="%d 개"
            )
        }
    )
    
    # 부품 추가 폼
    with st.form("add_part_form"):
        st.subheader(get_admin_text("add_part", lang))
        
        cols = st.columns(3)
        with cols[0]:
            part_code = st.text_input(get_admin_text("part_code", lang))
        
        with cols[1]:
            part_name = st.text_input(get_admin_text("part_name", lang))
        
        with cols[2]:
            initial_stock = st.number_input(
                get_admin_text("initial_stock", lang),
                min_value=0,
                value=0
            )
        
        if st.form_submit_button(get_admin_text("add_part", lang)):
            if not part_code or not part_name:
                st.error(get_admin_text("fill_all_fields", lang))
            else:
                st.success(f"'{part_name}' {get_admin_text('part_added', lang)}")
                st.rerun()

# 설비-시리얼 관리 탭 표시
def show_equipment_serial_management(lang):
    st.subheader(get_admin_text("equipment_serial_management", lang))
    
    # 현재 설비-시리얼 목록 조회
    serials = get_equipment_serials()
    
    # 데이터 표시
    if serials:
        df = pd.DataFrame(serials)
        df = df.rename(columns={
            'equipment_number': get_admin_text('equipment_number', lang),
            'serial_number': get_admin_text('serial_number', lang),
            'created_at': get_admin_text('creation_date', lang)
        })
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data available")
    
    # 작업 선택
    action = st.selectbox(
        "Action",
        ["Add", "Update", "Delete", "Bulk Upload"],
        format_func=lambda x: get_admin_text(f"{x.lower()}_equipment_serial", lang) if x != "Bulk Upload" else get_admin_text("bulk_upload", lang)
    )
    
    # 일괄 업로드
    if action == "Bulk Upload":
        st.subheader(get_admin_text("bulk_upload", lang))
        
        # 템플릿 다운로드 정보
        st.info(get_admin_text("template_info", lang))
        
        # 템플릿 다운로드 버튼
        if st.button(get_admin_text("download_template", lang)):
            template_csv = "equipment_number,serial_number\n1,800-001\n2,800-002\n"
            st.download_button(
                label=get_admin_text("download_template", lang),
                data=template_csv,
                file_name="equipment_serial_template.csv",
                mime="text/csv"
            )
        
        # CSV 형식 안내
        st.info(get_admin_text("csv_format", lang))
        
        # 파일 업로드
        uploaded_file = st.file_uploader(
            get_admin_text("upload_csv", lang),
            type=["csv"],
            key="equipment_serial_csv"
        )
        
        if uploaded_file is not None:
            try:
                # CSV 파일 파싱
                df = pd.read_csv(uploaded_file)
                
                # 필수 컬럼 확인
                if 'equipment_number' not in df.columns or 'serial_number' not in df.columns:
                    st.error("CSV 파일에 'equipment_number'와 'serial_number' 컬럼이 필요합니다.")
                else:
                    # 데이터 검증
                    if df['equipment_number'].isnull().any() or df['serial_number'].isnull().any():
                        st.error("빈 값이 있습니다. 모든 셀을 채워주세요.")
                    else:
                        # 데이터 변환
                        records = df.to_dict('records')
                        
                        # 데이터베이스에 일괄 업로드
                        result = bulk_upload_equipment_serials(records)
                        
                        if result:
                            st.success(f"{get_admin_text('upload_success', lang)}: {len(result)} records")
                            st.rerun()  # 페이지 새로고침
                        else:
                            st.error(get_admin_text("upload_error", lang))
            
            except Exception as e:
                st.error(f"{get_admin_text('upload_error', lang)}: {str(e)}")
    
    # 추가
    elif action == "Add":
        with st.form("add_equipment_serial_form"):
            st.subheader(get_admin_text("add_equipment_serial", lang))
            equipment_number = st.number_input(get_admin_text("equipment_number", lang), min_value=1, max_value=9999)
            serial_number = st.text_input(get_admin_text("serial_number", lang), value=f"800-{equipment_number:03d}")
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                # 중복 확인
                existing = get_serial_by_equipment_number(equipment_number)
                if existing:
                    st.error(get_admin_text("existing_equipment", lang))
                else:
                    result = add_equipment_serial(equipment_number, serial_number)
                    if result:
                        st.success(get_admin_text("add_success", lang))
                        st.rerun()  # 페이지 새로고침
    
    # 수정
    elif action == "Update":
        with st.form("update_equipment_serial_form"):
            st.subheader(get_admin_text("update_equipment_serial", lang))
            
            # 수정할 설비 선택
            equipment_options = [s['equipment_number'] for s in serials] if serials else []
            if not equipment_options:
                st.warning("수정할 설비가 없습니다.")
                st.form_submit_button("Submit", disabled=True)
            else:
                equipment_number = st.selectbox(
                    get_admin_text("equipment_number", lang),
                    options=equipment_options
                )
                
                # 현재 시리얼 번호 표시
                current_serial = next((s['serial_number'] for s in serials if s['equipment_number'] == equipment_number), "")
                new_serial = st.text_input(get_admin_text("serial_number", lang), value=current_serial)
                
                submitted = st.form_submit_button("Submit")
                
                if submitted and new_serial != current_serial:
                    result = update_equipment_serial(equipment_number, new_serial)
                    if result:
                        st.success(get_admin_text("update_success", lang))
                        st.rerun()  # 페이지 새로고침
    
    # 삭제
    elif action == "Delete":
        with st.form("delete_equipment_serial_form"):
            st.subheader(get_admin_text("delete_equipment_serial", lang))
            
            # 삭제할 설비 선택
            equipment_options = [s['equipment_number'] for s in serials] if serials else []
            if not equipment_options:
                st.warning("삭제할 설비가 없습니다.")
                st.form_submit_button("Submit", disabled=True)
            else:
                equipment_number = st.selectbox(
                    get_admin_text("equipment_number", lang),
                    options=equipment_options
                )
                
                confirm = st.checkbox(get_admin_text("confirm_delete", lang))
                
                submitted = st.form_submit_button("Submit")
                
                if submitted and confirm:
                    result = delete_equipment_serial(equipment_number)
                    if result:
                        st.success(get_admin_text("delete_success", lang))
                        st.rerun()  # 페이지 새로고침 