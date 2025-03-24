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