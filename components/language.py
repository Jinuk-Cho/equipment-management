"""
다국어 지원을 위한 모듈입니다.
한국어 및 베트남어 텍스트를 관리합니다.
"""

# 언어 텍스트 딕셔너리
TEXTS = {
    # 공통 UI 요소
    "system_title": {
        "ko": "설비 관리 시스템",
        "vi": "Hệ thống quản lý thiết bị"
    },
    "welcome": {
        "ko": "환영합니다!",
        "vi": "Xin chào!"
    },
    "login": {
        "ko": "로그인",
        "vi": "Đăng nhập"
    },
    "logout": {
        "ko": "로그아웃",
        "vi": "Đăng xuất"
    },
    "logout_help": {
        "ko": "로그아웃하기",
        "vi": "Đăng xuất"
    },
    "username": {
        "ko": "사용자",
        "vi": "Người dùng"
    },
    "login_time": {
        "ko": "로그인 시간",
        "vi": "Thời gian đăng nhập"
    },
    "session_expires": {
        "ko": "세션 만료까지",
        "vi": "Thời gian còn lại"
    },
    "email": {
        "ko": "이메일",
        "vi": "Email"
    },
    "password": {
        "ko": "비밀번호",
        "vi": "Mật khẩu"
    },
    "confirm_password": {
        "ko": "비밀번호 확인",
        "vi": "Xác nhận mật khẩu"
    },
    "login_failed": {
        "ko": "로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.",
        "vi": "Đăng nhập thất bại. Vui lòng kiểm tra email và mật khẩu."
    },
    "fill_all_fields": {
        "ko": "모든 필드를 입력해주세요.",
        "vi": "Vui lòng điền vào tất cả các trường."
    },
    "session_expired": {
        "ko": "세션이 만료되었습니다. 다시 로그인해주세요.",
        "vi": "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."
    },
    "register": {
        "ko": "회원가입",
        "vi": "Đăng ký"
    },
    "register_success": {
        "ko": "회원가입이 완료되었습니다. 로그인해주세요.",
        "vi": "Đăng ký thành công. Vui lòng đăng nhập."
    },
    "register_failed": {
        "ko": "회원가입에 실패했습니다. 다시 시도해주세요.",
        "vi": "Đăng ký thất bại. Vui lòng thử lại."
    },
    "password_mismatch": {
        "ko": "비밀번호가 일치하지 않습니다.",
        "vi": "Mật khẩu không khớp."
    },
    "name": {
        "ko": "이름",
        "vi": "Tên"
    },
    "department": {
        "ko": "부서",
        "vi": "Phòng ban"
    },
    "role": {
        "ko": "권한",
        "vi": "Quyền hạn"
    },
    "admin": {
        "ko": "관리자",
        "vi": "Quản trị viên"
    },
    "user": {
        "ko": "일반 사용자",
        "vi": "Người dùng"
    },
    "phone": {
        "ko": "전화번호",
        "vi": "Số điện thoại"
    },
    "profile": {
        "ko": "프로필",
        "vi": "Hồ sơ"
    },
    "save": {
        "ko": "저장",
        "vi": "Lưu"
    },
    "cancel": {
        "ko": "취소",
        "vi": "Hủy"
    },
    "edit": {
        "ko": "수정",
        "vi": "Chỉnh sửa"
    },
    "delete": {
        "ko": "삭제",
        "vi": "Xóa"
    },
    "create_new_account": {
        "ko": "새 계정 만들기",
        "vi": "Tạo tài khoản mới"
    },
    
    # 탭 이름
    "dashboard": {
        "ko": "대시보드",
        "vi": "Bảng điều khiển"
    },
    "equipment_detail": {
        "ko": "설비 상세",
        "vi": "Chi tiết thiết bị"
    },
    "data_input": {
        "ko": "데이터 입력",
        "vi": "Nhập dữ liệu"
    },
    "reports": {
        "ko": "보고서",
        "vi": "Báo cáo"
    },
    "admin_settings": {
        "ko": "관리자 설정",
        "vi": "Cài đặt quản trị"
    },
    
    # 대시보드 요소
    "equipment_status_distribution": {
        "ko": "설비 상태 분포",
        "vi": "Phân bố trạng thái thiết bị"
    },
    "error_distribution": {
        "ko": "고장 유형별 분포",
        "vi": "Phân bố theo loại lỗi"
    },
    "daily_errors": {
        "ko": "일별 고장 건수",
        "vi": "Số lượng lỗi hàng ngày"
    },
    "parts_replacement": {
        "ko": "부품별 교체 횟수",
        "vi": "Số lần thay thế theo linh kiện"
    },
    "average_repair_time": {
        "ko": "평균 수리 시간",
        "vi": "Thời gian sửa chữa trung bình"
    },
    "max_repair_time": {
        "ko": "최대 수리 시간",
        "vi": "Thời gian sửa chữa tối đa"
    },
    "total_downtime": {
        "ko": "총 다운타임",
        "vi": "Tổng thời gian dừng máy"
    },
    "minutes": {
        "ko": "분",
        "vi": "phút"
    },
    
    # 설비 상태
    "normal": {
        "ko": "정상",
        "vi": "Bình thường"
    },
    "inspection": {
        "ko": "점검중",
        "vi": "Đang kiểm tra"
    },
    "error": {
        "ko": "고장",
        "vi": "Hỏng"
    },
    
    # 오류 관련
    "error_code": {
        "ko": "오류 코드",
        "vi": "Mã lỗi"
    },
    "count": {
        "ko": "건수",
        "vi": "Số lượng"
    },
    "date": {
        "ko": "날짜",
        "vi": "Ngày"
    },
    
    # 부품 관련
    "part_code": {
        "ko": "부품 코드",
        "vi": "Mã linh kiện"
    },
    
    # 오류 메시지
    "admin_required": {
        "ko": "관리자 권한이 필요합니다.",
        "vi": "Yêu cầu quyền quản trị viên"
    },
    
    # 사용자 관리
    "user_management": {
        "ko": "사용자 관리",
        "vi": "Quản lý người dùng"
    },
    "user_list": {
        "ko": "사용자 목록",
        "vi": "Danh sách người dùng"
    },
    "add_user": {
        "ko": "사용자 추가",
        "vi": "Thêm người dùng"
    },
    "edit_user": {
        "ko": "사용자 편집",
        "vi": "Chỉnh sửa người dùng"
    },
    "delete_user": {
        "ko": "사용자 삭제",
        "vi": "Xóa người dùng"
    },
    "change_role": {
        "ko": "권한 변경",
        "vi": "Thay đổi quyền hạn"
    },
    "delete_confirm": {
        "ko": "정말 삭제하시겠습니까?",
        "vi": "Bạn có chắc chắn muốn xóa không?"
    },
    "user_deleted": {
        "ko": "사용자가 삭제되었습니다.",
        "vi": "Người dùng đã bị xóa."
    },
    "user_added": {
        "ko": "사용자가 추가되었습니다.",
        "vi": "Người dùng đã được thêm."
    },
    "user_updated": {
        "ko": "사용자 정보가 업데이트되었습니다.",
        "vi": "Thông tin người dùng đã được cập nhật."
    },
    "last_login": {
        "ko": "마지막 로그인",
        "vi": "Đăng nhập lần cuối"
    },
    "created_at": {
        "ko": "생성일",
        "vi": "Ngày tạo"
    }
}

def get_text(key, lang):
    """
    지정된 키에 대한 텍스트를 선택한 언어로 반환합니다.
    
    Args:
        key (str): 텍스트 키
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        str: 선택한 언어의 텍스트
    """
    if key in TEXTS:
        return TEXTS[key].get(lang, TEXTS[key]['ko'])  # 기본값은 한국어
    return f"[{key}]"  # 키가 없는 경우 키 자체를 반환 