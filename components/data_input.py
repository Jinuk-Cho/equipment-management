try:
    import streamlit as st
except ImportError:
    print("ERROR: 'streamlit' package is not installed. Please install it using: pip install streamlit")
    # 임시 대체 모듈
    class StMock:
        def __getattr__(self, name):
            def dummy(*args, **kwargs):
                return None
            return dummy
    st = StMock()

try:
    import pandas as pd
except ImportError:
    print("ERROR: 'pandas' package is not installed. Please install it using: pip install pandas")
    # 임시 대체 모듈
    import csv
    class PdMock:
        def __getattr__(self, name):
            def dummy(*args, **kwargs):
                return None
            return dummy
    pd = PdMock()

from datetime import datetime, timedelta
import os
import json
import uuid

try:
    from utils.supabase_client import add_error_history, add_parts_replacement, get_serial_by_equipment_number, add_model_change, insert_data, add_equipment_stop
except ImportError:
    print("ERROR: 'utils.supabase_client' module not found.")
    # 임시 대체 함수들
    def add_error_history(*args, **kwargs): return None
    def add_parts_replacement(*args, **kwargs): return None
    def get_serial_by_equipment_number(*args, **kwargs): return None
    def add_model_change(*args, **kwargs): return None
    def insert_data(*args, **kwargs): return None
    def add_equipment_stop(*args, **kwargs): return None

try:
    from components.language import _normalize_language_code, get_text
except ImportError:
    print("ERROR: 'components.language' module not found.")
    # 임시 대체 함수
    def get_text(*args, **kwargs): return args[0]

try:
    from PIL import Image
    import io
except ImportError:
    print("ERROR: 'Pillow' package is not installed. Please install it using: pip install Pillow")
    # 임시 대체 모듈
    class ImageMock:
        def __getattr__(self, name):
            def dummy(*args, **kwargs):
                return None
            return dummy
    Image = ImageMock()
    io = __import__('io')

# 데이터 입력 페이지 텍스트
DATA_INPUT_TEXTS = {
    "data_input": {
        "ko": "데이터 입력",
        "vi": "Nhập dữ liệu"
    },
    "equipment_number": {
        "ko": "설비 번호",
        "vi": "Số thiết bị"
    },
    "serial_number": {
        "ko": "시리얼 번호",
        "vi": "Số serial"
    },
    "serial_number_auto": {
        "ko": "시리얼 번호 (자동 입력)",
        "vi": "Số serial (tự động điền)"
    },
    "error_code": {
        "ko": "오류 코드",
        "vi": "Mã lỗi"
    },
    "error_detail": {
        "ko": "오류 상세 내용",
        "vi": "Chi tiết lỗi"
    },
    "repair_time": {
        "ko": "수리 시간 (분)",
        "vi": "Thời gian sửa chữa (phút)"
    },
    "part_code": {
        "ko": "부품 코드",
        "vi": "Mã linh kiện"
    },
    "worker": {
        "ko": "작업자",
        "vi": "Người thực hiện"
    },
    "supervisor": {
        "ko": "감독자",
        "vi": "Người giám sát"
    },
    "related_images": {
        "ko": "관련 이미지",
        "vi": "Hình ảnh liên quan"
    },
    "select_images": {
        "ko": "이미지 파일 선택 (최대 10개)",
        "vi": "Chọn file hình ảnh (tối đa 10 file)"
    },
    "image_preview": {
        "ko": "이미지 미리보기",
        "vi": "Xem trước hình ảnh"
    },
    "image": {
        "ko": "이미지",
        "vi": "Hình ảnh"
    },
    "save": {
        "ko": "저장",
        "vi": "Lưu"
    },
    "fill_all_fields": {
        "ko": "모든 필드를 입력해주세요.",
        "vi": "Vui lòng điền vào tất cả các trường"
    },
    "save_success": {
        "ko": "데이터가 데이터베이스에 성공적으로 저장되었습니다.",
        "vi": "Dữ liệu đã được lưu thành công vào cơ sở dữ liệu"
    },
    "save_session_only": {
        "ko": "데이터가 현재 세션에만 저장되었고 데이터베이스에는 저장되지 않았습니다.",
        "vi": "Dữ liệu đã được lưu trong phiên hiện tại nhưng không lưu vào cơ sở dữ liệu"
    },
    "save_error": {
        "ko": "데이터베이스 저장 오류",
        "vi": "Lỗi khi lưu vào cơ sở dữ liệu"
    },
    "save_session": {
        "ko": "데이터가 현재 세션에만 저장되었습니다.",
        "vi": "Dữ liệu đã được lưu trong phiên hiện tại"
    },
    "input_history": {
        "ko": "입력 내역",
        "vi": "Lịch sử nhập dữ liệu"
    },
    "input_time": {
        "ko": "입력 시간",
        "vi": "Thời gian nhập"
    },
    "minutes": {
        "ko": "분",
        "vi": "phút"
    },
    "image_count": {
        "ko": "이미지 수량",
        "vi": "Số lượng hình ảnh"
    },
    "qr_scan": {
        "ko": "QR 코드 스캔",
        "vi": "Quét mã QR"
    },
    "qr_info": {
        "ko": "모바일에서 QR 코드를 스캔하면 자동으로 설비 정보가 입력됩니다.",
        "vi": "Khi quét mã QR trên thiết bị di động, thông tin thiết bị sẽ được tự động điền"
    },
    "equipment_no_info": {
        "ko": "설비 번호를 입력하면 시리얼 번호가 자동으로 입력됩니다.",
        "vi": "Khi nhập số thiết bị, số serial sẽ được tự động điền"
    },
    "no_serial_found": {
        "ko": "해당 설비 번호에 대한 시리얼 번호 정보가 없습니다.",
        "vi": "Không có thông tin số serial cho số thiết bị này"
    },
    "stop_reason": {
        "ko": "정지 사유",
        "vi": "Lý do dừng"
    },
    "stop_reason_pm": {
        "ko": "PM",
        "vi": "PM"
    },
    "stop_reason_model_change": {
        "ko": "모델 교체",
        "vi": "Thay đổi mô hình"
    },
    "stop_reason_material_wait": {
        "ko": "자재대기",
        "vi": "Chờ vật liệu"
    },
    "stop_reason_planned": {
        "ko": "계획 정지",
        "vi": "Dừng theo kế hoạch"
    },
    "stop_start_time": {
        "ko": "정지 시작 시간",
        "vi": "Thời gian bắt đầu dừng"
    },
    "stop_end_time": {
        "ko": "정지 종료 시간",
        "vi": "Thời gian kết thúc dừng"
    },
    "stop_duration": {
        "ko": "정지 시간 (분)",
        "vi": "Thời gian dừng (phút)"
    },
    "model_name_from": {
        "ko": "이전 모델명",
        "vi": "Tên mô hình trước"
    },
    "model_name_to": {
        "ko": "변경 모델명",
        "vi": "Tên mô hình sau"
    },
    "model_change_details": {
        "ko": "모델 변경 상세 내용",
        "vi": "Chi tiết thay đổi mô hình"
    }
}

def get_input_text(key, lang):
    """데이터 입력 페이지 전용 텍스트를 가져옵니다."""
    if key in DATA_INPUT_TEXTS:
        return DATA_INPUT_TEXTS[key].get(lang, DATA_INPUT_TEXTS[key]['ko'])
    return f"[{key}]"

# 설비 번호와 시리얼 번호 매핑 - 기본 백업용 매핑
# 데이터베이스 연결이 실패한 경우 사용됨
DEFAULT_EQUIPMENT_SERIAL_MAPPING = {}

# 800대 설비에 대한 시리얼 번호 매핑 자동 생성
for i in range(1, 801):
    DEFAULT_EQUIPMENT_SERIAL_MAPPING[i] = f"800-{i:03d}"

def get_serial_number(equipment_number):
    """설비 번호에 해당하는 시리얼 번호를 반환합니다.
    먼저 데이터베이스에서 조회하고, 없으면 기본 매핑에서 가져옵니다."""
    
    # 1. 데이터베이스에서 시리얼 번호 조회 시도
    db_serial = get_serial_by_equipment_number(equipment_number)
    if db_serial:
        return db_serial
    
    # 2. 데이터베이스에서 찾지 못한 경우 기본 매핑 사용
    return DEFAULT_EQUIPMENT_SERIAL_MAPPING.get(equipment_number, None)

# 이미지 압축 함수
def compress_image(file, max_size=1024, quality=85):
    """이미지를 압축하여 메모리 사용량을 줄입니다."""
    # 이미지 열기
    img = Image.open(file)
    
    # RGBA 이미지를 RGB로 변환 (JPG는 알파 채널을 지원하지 않음)
    if img.mode == 'RGBA':
        # 흰색 배경에 합성
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])  # 알파 채널을 마스크로 사용
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 이미지 크기 확인 및 조정
    w, h = img.size
    if max(w, h) > max_size:
        if w > h:
            new_w, new_h = max_size, int(h * max_size / w)
        else:
            new_w, new_h = int(w * max_size / h), max_size
        # LANCZOS 대신 호환성 있는 리사이징 필터 사용
        try:
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        except AttributeError:
            # 구버전 Pillow에서는 ANTIALIAS 사용
            img = img.resize((new_w, new_h), Image.ANTIALIAS)
    
    # 압축된 이미지를 바이트로 변환
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    
    return buffer

class DataInputComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'ko'
        
    def render(self):
        """데이터 입력 페이지를 표시합니다."""
        # 언어 코드 표준화
        lang = _normalize_language_code(self.lang)
        if 'current_lang' in st.session_state:
            lang = _normalize_language_code(st.session_state.current_lang)
        
        st.title(get_input_text("data_input", lang))
        
        # 입력 유형 선택
        input_tabs = st.tabs([
            get_input_text("error_input", lang),
            get_input_text("parts_input", lang),
            get_input_text("model_change_input", lang),
            get_input_text("equipment_stop_input", lang)
        ])
        
        # 오류 입력 탭
        with input_tabs[0]:
            self.render_error_input(lang)
            
        # 부품교체 입력 탭
        with input_tabs[1]:
            self.render_parts_input(lang)
            
        # 모델교체 입력 탭
        with input_tabs[2]:
            self.render_model_change_input(lang)
            
        # 설비 정지 입력 탭
        with input_tabs[3]:
            self.render_equipment_stop_input(lang)
    
    def render_error_input(self, lang):
        """오류 입력 폼을 렌더링합니다."""
        with st.form("error_input_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                equipment_number = st.text_input(get_input_text("equipment_number", lang))
                st.caption(get_input_text("equipment_no_info", lang))
                
                serial_number = st.text_input(
                    get_input_text("serial_number_auto", lang),
                    disabled=True
                )
                
                error_code = st.text_input(get_input_text("error_code", lang))
                
            with col2:
                error_detail = st.text_area(get_input_text("error_detail", lang))
                repair_time = st.number_input(
                    get_input_text("repair_time", lang),
                    min_value=1,
                    value=30
                )
                
            col3, col4 = st.columns(2)
            with col3:
                worker = st.text_input(get_input_text("worker", lang))
            with col4:
                supervisor = st.text_input(get_input_text("supervisor", lang))
        
            # 이미지 파일 업로더
            st.subheader(get_input_text("related_images", lang))
            uploaded_files = st.file_uploader(
                get_input_text("select_images", lang),
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True
            )
            
            # 이미지 미리보기
            if uploaded_files:
                st.subheader(get_input_text("image_preview", lang))
                image_cols = st.columns(min(len(uploaded_files), 4))
                
                for i, file in enumerate(uploaded_files[:10]):  # 최대 10개까지만 표시
                    with image_cols[i % 4]:
                        img = Image.open(file)
                        st.image(img, caption=f"{get_input_text('image', lang)} {i+1}", width=150)
            
            # 설비 번호 입력 시 시리얼 번호 자동 조회
            if equipment_number:
                serial = get_serial_number(equipment_number)
                if serial:
                    serial_number = serial
                    st.session_state.serial_number = serial
                else:
                    st.warning(get_input_text("no_serial_found", lang))
            
            # 폼 제출 버튼
            submitted = st.form_submit_button(get_input_text("save", lang))
            
            if submitted:
                # 필수 필드 검증
                if not all([equipment_number, error_code, error_detail, worker, supervisor]):
                    st.error(get_input_text("fill_all_fields", lang))
                else:
                    try:
                        # 이미지 처리
                        image_data = []
                        if uploaded_files:
                            for file in uploaded_files[:10]:  # 최대 10개까지만 저장
                                compressed_image = compress_image(file)
                                image_data.append({
                                    "filename": file.name,
                                    "image_data": compressed_image
                                })
                        
                        # 데이터 저장
                        add_error_history(
                            equipment_number=equipment_number,
                            serial_number=serial_number or "",
                            error_code=error_code,
                            error_detail=error_detail,
                            repair_time=repair_time,
                            worker=worker,
                            supervisor=supervisor,
                            images=image_data
                        )
                        
                        st.success(get_input_text("save_success", lang))
                        
                        # 저장 후 폼 초기화
                        st.session_state.equipment_number = ""
                        st.session_state.serial_number = ""
                        st.session_state.error_code = ""
                        st.session_state.error_detail = ""
                        st.session_state.repair_time = 30
                        st.session_state.worker = ""
                        st.session_state.supervisor = ""
                        
                    except Exception as e:
                        st.error(f"{get_input_text('save_error', lang)}: {str(e)}")
                        # 로컬 세션에 저장
                        if 'error_history' not in st.session_state:
                            st.session_state.error_history = []
                        
                        st.session_state.error_history.append({
                            "timestamp": datetime.now(),
                            "equipment_number": equipment_number,
                            "serial_number": serial_number or "",
                            "error_code": error_code,
                            "error_detail": error_detail,
                            "repair_time": repair_time,
                            "worker": worker,
                            "supervisor": supervisor,
                            "image_count": len(uploaded_files) if uploaded_files else 0
                        })
                        
                        st.info(get_input_text("save_session", lang))
        
        # 입력 내역 표시
        if 'error_history' in st.session_state and st.session_state.error_history:
            st.subheader(get_input_text("input_history", lang))
            
            for i, entry in enumerate(st.session_state.error_history):
                with st.expander(f"#{i+1} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"{get_input_text('equipment_number', lang)}: {entry['equipment_number']}")
                        st.write(f"{get_input_text('serial_number', lang)}: {entry['serial_number']}")
                        st.write(f"{get_input_text('error_code', lang)}: {entry['error_code']}")
                    
                    with col2:
                        st.write(f"{get_input_text('error_detail', lang)}: {entry['error_detail']}")
                        st.write(f"{get_input_text('repair_time', lang)}: {entry['repair_time']} {get_input_text('minutes', lang)}")
                        st.write(f"{get_input_text('worker', lang)}: {entry['worker']}")
                        st.write(f"{get_input_text('supervisor', lang)}: {entry['supervisor']}")
                        if 'image_count' in entry and entry['image_count'] > 0:
                            st.write(f"{get_input_text('image_count', lang)}: {entry['image_count']}")
    
    def render_parts_input(self, lang):
        """부품 교체 입력 폼을 렌더링합니다."""
        with st.form("parts_input_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                parts_equipment_number = st.text_input(get_input_text("equipment_number", lang), key="parts_equipment_number")
                st.caption(get_input_text("equipment_no_info", lang))
                
                parts_serial_number = st.text_input(
                    get_input_text("serial_number_auto", lang),
                    disabled=True,
                    key="parts_serial_number"
                )
                
                part_code = st.text_input(get_input_text("part_code", lang))
                
            with col2:
                parts_repair_time = st.number_input(
                    get_input_text("repair_time", lang),
                    min_value=1,
                    value=30,
                    key="parts_repair_time"
                )
                
            col3, col4 = st.columns(2)
            with col3:
                parts_worker = st.text_input(get_input_text("worker", lang), key="parts_worker")
            with col4:
                parts_supervisor = st.text_input(get_input_text("supervisor", lang), key="parts_supervisor")
            
            # 이미지 파일 업로더
            st.subheader(get_input_text("related_images", lang))
            parts_uploaded_files = st.file_uploader(
                get_input_text("select_images", lang),
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="parts_uploaded_files"
            )
            
            # 이미지 미리보기
            if parts_uploaded_files:
                st.subheader(get_input_text("image_preview", lang))
                image_cols = st.columns(min(len(parts_uploaded_files), 4))
                
                for i, file in enumerate(parts_uploaded_files[:10]):  # 최대 10개까지만 표시
                    with image_cols[i % 4]:
                        img = Image.open(file)
                        st.image(img, caption=f"{get_input_text('image', lang)} {i+1}", width=150)
            
            # 설비 번호 입력 시 시리얼 번호 자동 조회
            if parts_equipment_number:
                serial = get_serial_number(parts_equipment_number)
                if serial:
                    parts_serial_number = serial
                    st.session_state.parts_serial_number = serial
                else:
                    st.warning(get_input_text("no_serial_found", lang))
            
            # 폼 제출 버튼
            parts_submitted = st.form_submit_button(get_input_text("save", lang))
            
            if parts_submitted:
                # 필수 필드 검증
                if not all([parts_equipment_number, part_code, parts_worker, parts_supervisor]):
                    st.error(get_input_text("fill_all_fields", lang))
                else:
                    try:
                        # 이미지 처리
                        image_data = []
                        if parts_uploaded_files:
                            for file in parts_uploaded_files[:10]:  # 최대 10개까지만 저장
                                compressed_image = compress_image(file)
                                image_data.append({
                                    "filename": file.name,
                                    "image_data": compressed_image
                                })
                        
                        # 데이터 저장
                        add_parts_replacement(
                            equipment_number=parts_equipment_number,
                            serial_number=parts_serial_number or "",
                            part_code=part_code,
                            repair_time=parts_repair_time,
                            worker=parts_worker,
                            supervisor=parts_supervisor,
                            images=image_data
                        )
                        
                        st.success(get_input_text("save_success", lang))
                        
                        # 저장 후 폼 초기화
                        st.session_state.parts_equipment_number = ""
                        st.session_state.parts_serial_number = ""
                        st.session_state.part_code = ""
                        st.session_state.parts_repair_time = 30
                        st.session_state.parts_worker = ""
                        st.session_state.parts_supervisor = ""
                        
                    except Exception as e:
                        st.error(f"{get_input_text('save_error', lang)}: {str(e)}")
                        # 로컬 세션에 저장
                        if 'parts_history' not in st.session_state:
                            st.session_state.parts_history = []
                        
                        st.session_state.parts_history.append({
                            "timestamp": datetime.now(),
                            "equipment_number": parts_equipment_number,
                            "serial_number": parts_serial_number or "",
                            "part_code": part_code,
                            "repair_time": parts_repair_time,
                            "worker": parts_worker,
                            "supervisor": parts_supervisor,
                            "image_count": len(parts_uploaded_files) if parts_uploaded_files else 0
                        })
                        
                        st.info(get_input_text("save_session", lang))
        
        # 입력 내역 표시
        if 'parts_history' in st.session_state and st.session_state.parts_history:
            st.subheader(get_input_text("input_history", lang))
            
            for i, entry in enumerate(st.session_state.parts_history):
                with st.expander(f"#{i+1} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"{get_input_text('equipment_number', lang)}: {entry['equipment_number']}")
                        st.write(f"{get_input_text('serial_number', lang)}: {entry['serial_number']}")
                        st.write(f"{get_input_text('part_code', lang)}: {entry['part_code']}")
                    
                    with col2:
                        st.write(f"{get_input_text('repair_time', lang)}: {entry['repair_time']} {get_input_text('minutes', lang)}")
                        st.write(f"{get_input_text('worker', lang)}: {entry['worker']}")
                        st.write(f"{get_input_text('supervisor', lang)}: {entry['supervisor']}")
                        if 'image_count' in entry and entry['image_count'] > 0:
                            st.write(f"{get_input_text('image_count', lang)}: {entry['image_count']}")
    
    def render_model_change_input(self, lang):
        """모델 교체 입력 폼을 렌더링합니다."""
        with st.form("model_change_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                model_equipment_number = st.text_input(get_input_text("equipment_number", lang), key="model_equipment_number")
                from_model = st.text_input("이전 모델", key="from_model")
                
            with col2:
                to_model = st.text_input("변경 모델", key="to_model")
                model_change_time = st.number_input(
                    "모델 교체 시간 (분)",
                    min_value=1,
                    value=30,
                    key="model_change_time"
                )
                
            col3, col4 = st.columns(2)
            with col3:
                model_worker = st.text_input(get_input_text("worker", lang), key="model_worker")
            with col4:
                model_supervisor = st.text_input(get_input_text("supervisor", lang), key="model_supervisor")
            
            # 폼 제출 버튼
            model_submitted = st.form_submit_button(get_input_text("save", lang))
            
            if model_submitted:
                # 필수 필드 검증
                if not all([model_equipment_number, from_model, to_model, model_worker, model_supervisor]):
                    st.error(get_input_text("fill_all_fields", lang))
                else:
                    try:
                        # 데이터 저장
                        add_model_change(
                            equipment_number=model_equipment_number,
                            from_model=from_model,
                            to_model=to_model,
                            change_time=model_change_time,
                            worker=model_worker,
                            supervisor=model_supervisor
                        )
                        
                        st.success(get_input_text("save_success", lang))
                        
                        # 저장 후 폼 초기화
                        st.session_state.model_equipment_number = ""
                        st.session_state.from_model = ""
                        st.session_state.to_model = ""
                        st.session_state.model_change_time = 30
                        st.session_state.model_worker = ""
                        st.session_state.model_supervisor = ""
                        
                    except Exception as e:
                        st.error(f"{get_input_text('save_error', lang)}: {str(e)}")
                        # 로컬 세션에 저장
                        if 'model_change_history' not in st.session_state:
                            st.session_state.model_change_history = []
                        
                        st.session_state.model_change_history.append({
                            "timestamp": datetime.now(),
                            "equipment_number": model_equipment_number,
                            "from_model": from_model,
                            "to_model": to_model,
                            "change_time": model_change_time,
                            "worker": model_worker,
                            "supervisor": model_supervisor
                        })
                        
                        st.info(get_input_text("save_session", lang))
    
    def render_equipment_stop_input(self, lang):
        """설비 정지 입력 폼을 렌더링합니다."""
        with st.form("equipment_stop_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                stop_equipment_number = st.text_input(get_input_text("equipment_number", lang), key="stop_equipment_number")
                
                stop_reason = st.selectbox(
                    get_input_text("stop_reason", lang),
                    [
                        get_input_text("stop_reason_pm", lang),
                        get_input_text("stop_reason_model_change", lang),
                        get_input_text("stop_reason_material_wait", lang),
                        get_input_text("stop_reason_planned", lang)
                    ],
                    key="stop_reason"
                )
                
            with col2:
                # datetime_input 대신 date_input과 time_input 사용
                stop_date = st.date_input(
                    "정지 날짜",
                    value=datetime.now().date(),
                    key="stop_date"
                )
                
                stop_time = st.time_input(
                    "정지 시각",
                    value=datetime.now().time(),
                    key="stop_time"
                )
                
                # 날짜와 시간을 합쳐서 datetime 객체 생성
                stop_start_time = datetime.combine(stop_date, stop_time)
                
                stop_duration = st.number_input(
                    "정지 시간 (분)",
                    min_value=1,
                    value=30,
                    key="stop_duration"
                )
                
            col3, col4 = st.columns(2)
            with col3:
                stop_worker = st.text_input(get_input_text("worker", lang), key="stop_worker")
            with col4:
                stop_supervisor = st.text_input(get_input_text("supervisor", lang), key="stop_supervisor")
            
            # 추가 설명
            stop_detail = st.text_area("추가 설명", key="stop_detail")
            
            # 폼 제출 버튼
            stop_submitted = st.form_submit_button(get_input_text("save", lang))
            
            if stop_submitted:
                # 필수 필드 검증
                if not all([stop_equipment_number, stop_worker, stop_supervisor]):
                    st.error(get_input_text("fill_all_fields", lang))
                else:
                    try:
                        # 데이터 저장
                        add_equipment_stop(
                            equipment_number=stop_equipment_number,
                            stop_reason=stop_reason,
                            start_time=stop_start_time,
                            duration_minutes=stop_duration,
                            worker=stop_worker,
                            supervisor=stop_supervisor,
                            details=stop_detail
                        )
                        
                        st.success(get_input_text("save_success", lang))
                        
                        # 저장 후 폼 초기화
                        st.session_state.stop_equipment_number = ""
                        st.session_state.stop_reason = get_input_text("stop_reason_pm", lang)
                        st.session_state.stop_date = datetime.now().date()
                        st.session_state.stop_time = datetime.now().time()
                        st.session_state.stop_duration = 30
                        st.session_state.stop_worker = ""
                        st.session_state.stop_supervisor = ""
                        st.session_state.stop_detail = ""
                        
                    except Exception as e:
                        st.error(f"{get_input_text('save_error', lang)}: {str(e)}")
                        # 로컬 세션에 저장
                        if 'equipment_stop_history' not in st.session_state:
                            st.session_state.equipment_stop_history = []
                        
                        st.session_state.equipment_stop_history.append({
                            "timestamp": datetime.now(),
                            "equipment_number": stop_equipment_number,
                            "stop_reason": stop_reason,
                            "start_time": stop_start_time,
                            "duration": stop_duration,
                            "worker": stop_worker,
                            "supervisor": stop_supervisor,
                            "details": stop_detail
                        })
                        
                    st.info(get_input_text("save_session", lang))
    

# 원래 함수는 주석 처리합니다
# def show_data_input(lang='ko'):
#     """데이터 입력 페이지를 표시합니다."""
#     st.title(get_input_text("data_input", lang))
#     // ... rest of the original function ...

# Supabase에서 설비 정보를 가져오는 함수
def get_equipment_from_supabase(equipment_number, serial_number=None):
    """
    Supabase에서 설비 정보를 가져오는 함수
    나중에 실제 데이터베이스 연동할 때 구현할 것
    """
    # TODO: 실제 Supabase 연동 코드로 대체 필요
    return {
        "equipment_number": f"EQ{equipment_number:03d}",
        "serial_number": serial_number or DEFAULT_EQUIPMENT_SERIAL_MAPPING.get(equipment_number, ""),
        "equipment_type": "프레스" if equipment_number % 3 == 0 else "컨베이어" if equipment_number % 3 == 1 else "로봇",
        "building": f"{chr(65 + (equipment_number % 3))}동",
        "status": "정상" if equipment_number % 4 != 0 else "점검중"
    }

# 파일이 직접 실행될 때 작동하는 메인 함수 추가
if __name__ == "__main__":
    print("데이터 입력 모듈이 성공적으로 로드되었습니다.")
    print("이 모듈은 필요한 모든 패키지를 설치한 후 사용할 수 있습니다.")
    print("필요한 패키지: streamlit, pandas, Pillow")
    print("설치 명령어: pip install streamlit pandas Pillow") 