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
    from components.language import get_text
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
    
    # 이미지 크기 확인 및 조정
    w, h = img.size
    if max(w, h) > max_size:
        if w > h:
            new_w, new_h = max_size, int(h * max_size / w)
        else:
            new_w, new_h = int(w * max_size / h), max_size
        img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # 압축된 이미지를 바이트로 변환
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    
    return buffer

def show_data_input(lang='ko'):
    """데이터 입력 페이지를 표시합니다."""
    st.title(get_input_text("data_input", lang))
    
    # 세션 상태에 입력 내역 저장하기 위한 초기화
    if 'input_history' not in st.session_state:
        st.session_state.input_history = []
    
    # 설비 번호를 위한 상태 초기화
    if 'equipment_number' not in st.session_state:
        st.session_state.equipment_number = 1
    
    # 시리얼 번호를 위한 상태 초기화
    if 'serial_number' not in st.session_state:
        st.session_state.serial_number = get_serial_number(1)
    
    # 설비 번호에 따른 시리얼 번호 자동 업데이트 함수
    def update_serial_number():
        equipment_number = st.session_state.equipment_number
        serial = get_serial_number(equipment_number)
        if serial:
            st.session_state.serial_number = serial
        else:
            st.session_state.serial_number = get_input_text("no_serial_found", lang)
    
    # 예시 데이터
    error_codes = ['E001', 'E002', 'E003', 'E004', 'E005']
    parts_list = ['P001', 'P002', 'P003', 'P004']
    
    # 설명 추가
    st.info(get_input_text("equipment_no_info", lang))
    
    # 폼 외부에서 설비 번호 입력 받기
    eq_num_col1, eq_num_col2 = st.columns([1, 3])
    with eq_num_col1:
        temp_equipment_number = st.number_input(
            get_input_text("equipment_number", lang),
            min_value=1,
            max_value=800,
            value=st.session_state.equipment_number,
            step=1,
            key="temp_equipment_number",
            on_change=update_serial_number
        )
    
    # 폼 외부에서 설비 번호 변경 시 세션 상태 업데이트
    if temp_equipment_number != st.session_state.equipment_number:
        st.session_state.equipment_number = temp_equipment_number
        st.session_state.serial_number = get_serial_number(temp_equipment_number) or get_input_text("no_serial_found", lang)
    
    with eq_num_col2:
        st.text_input(
            get_input_text("serial_number_auto", lang),
            value=st.session_state.serial_number,
            disabled=True,
            key="temp_serial_number"
        )
    
    # 입력 폼
    with st.form("data_input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # 폼 내에서는 세션 상태의 값을 사용
            st.text_input(
                get_input_text("equipment_number", lang),
                value=str(st.session_state.equipment_number),
                disabled=True,
                key="form_equipment_number"
            )
            
            st.text_input(
                get_input_text("serial_number_auto", lang),
                value=st.session_state.serial_number,
                disabled=True,
                key="form_serial_number"
            )
            
            error_code = st.selectbox(get_input_text("error_code", lang), error_codes)
            error_detail = st.text_area(get_input_text("error_detail", lang))
        
        with col2:
            # 정지 사유 선택 추가
            stop_reasons = [
                get_input_text("stop_reason_pm", lang),
                get_input_text("stop_reason_model_change", lang),
                get_input_text("stop_reason_material_wait", lang),
                get_input_text("stop_reason_planned", lang)
            ]
            
            stop_reason = st.selectbox(
                get_input_text("stop_reason", lang),
                options=stop_reasons
            )
            
            # 정지 시작 시간 (기본값: 현재 시간)
            stop_start_time = st.datetime_input(
                get_input_text("stop_start_time", lang),
                value=datetime.now()
            )
            
            # 정지 종료 시간 (선택 사항)
            stop_end_time = st.datetime_input(
                get_input_text("stop_end_time", lang),
                value=datetime.now() + timedelta(minutes=30)
            )
            
            # 정지 시간 계산 및 표시 (분 단위)
            if stop_end_time > stop_start_time:
                duration_minutes = (stop_end_time - stop_start_time).total_seconds() / 60
                stop_duration = st.number_input(
                    get_input_text("stop_duration", lang),
                    value=int(duration_minutes),
                    step=1,
                    min_value=1
                )
            else:
                st.error("종료 시간은 시작 시간보다 이후여야 합니다.")
                stop_duration = 0
            
            # 선택된 정지 사유가 모델 교체인 경우 추가 입력 필드 표시
            if stop_reason == get_input_text("stop_reason_model_change", lang):
                # 샘플 모델명 리스트
                model_list = ['M001', 'M002', 'M003', 'M004', 'M005', 'M006']
                
                model_from = st.selectbox(
                    get_input_text("model_name_from", lang),
                    options=model_list
                )
                
                model_to = st.selectbox(
                    get_input_text("model_name_to", lang),
                    options=model_list
                )
                
                model_change_details = st.text_area(
                    get_input_text("model_change_details", lang),
                    height=100
                )
            
            repair_time = st.number_input(get_input_text("repair_time", lang), min_value=1, max_value=480)
            part_code = st.selectbox(get_input_text("part_code", lang), parts_list)
            worker = st.text_input(get_input_text("worker", lang))
            supervisor = st.text_input(get_input_text("supervisor", lang))
        
        # 이미지 업로드 (최대 10개로 제한)
        st.subheader(get_input_text("related_images", lang))
        uploaded_files = st.file_uploader(
            get_input_text("select_images", lang),
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True
        )
        
        # 이미지 미리보기 (최대 10개만 표시)
        if uploaded_files:
            st.subheader(get_input_text("image_preview", lang))
            # 10개로 제한
            limited_files = uploaded_files[:10]
            if len(uploaded_files) > 10:
                st.warning(f"최대 10개의 이미지만 업로드할 수 있습니다. 처음 10개만 사용됩니다.")
            
            cols = st.columns(5)
            for idx, file in enumerate(limited_files):
                with cols[idx % 5]:
                    st.image(file, use_column_width=True)
                    st.caption(f"{get_input_text('image', lang)} {idx + 1}")
        
        submitted = st.form_submit_button(get_input_text("save", lang))
        
        if submitted:
            if not all([str(st.session_state.equipment_number), st.session_state.serial_number, error_code, error_detail, repair_time, worker, supervisor]):
                st.error(get_input_text("fill_all_fields", lang))
            else:
                # 이미지 저장
                image_paths = []
                if uploaded_files:
                    save_dir = f"uploads/{datetime.now().strftime('%Y%m%d')}"
                    os.makedirs(save_dir, exist_ok=True)
                    
                    # 10개로 제한
                    limited_files = uploaded_files[:10]
                    
                    for idx, file in enumerate(limited_files):
                        # 이미지 압축
                        try:
                            compressed_file = compress_image(file)
                            file_path = os.path.join(save_dir, f"{st.session_state.equipment_number}_{datetime.now().strftime('%H%M%S')}_{idx+1}.jpg")
                            with open(file_path, "wb") as f:
                                f.write(compressed_file.getbuffer())
                            image_paths.append(file_path)
                        except Exception as e:
                            st.error(f"이미지 압축 중 오류 발생: {str(e)}")
                            # 압축 실패 시 원본 이미지 저장
                            file_path = os.path.join(save_dir, f"{st.session_state.equipment_number}_{datetime.now().strftime('%H%M%S')}_{idx+1}{os.path.splitext(file.name)[1]}")
                            with open(file_path, "wb") as f:
                                f.write(file.getbuffer())
                            image_paths.append(file_path)

                # 입력 데이터 생성
                timestamp = datetime.now()
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # 설비 번호 포맷 (예: EQ001)
                formatted_equipment = f"EQ{st.session_state.equipment_number:03d}"
                
                # 세션용 데이터
                session_data = {
                    "timestamp": timestamp_str,
                    "equipment": formatted_equipment,
                    "serial_number": st.session_state.serial_number,
                    "error_code": error_code,
                    "error_detail": error_detail,
                    "repair_time": repair_time,
                    "part_code": part_code,
                    "worker": worker,
                    "supervisor": supervisor,
                    "images": len(image_paths)
                }
                
                # Supabase용 에러 히스토리 데이터
                error_data = {
                    "timestamp": timestamp_str,
                    "equipment_number": formatted_equipment,
                    "serial_number": st.session_state.serial_number,
                    "error_code": error_code,
                    "error_detail": error_detail,
                    "repair_time": repair_time,
                    "repair_method": f"부품 {part_code} 교체",
                    "worker": worker,
                    "supervisor": supervisor,
                    "image_paths": ",".join(image_paths) if image_paths else ""
                }
                
                # Supabase용 부품 교체 데이터
                parts_data = {
                    "timestamp": timestamp_str,
                    "equipment_number": formatted_equipment,
                    "serial_number": st.session_state.serial_number,
                    "part_code": part_code,
                    "worker": worker,
                    "supervisor": supervisor
                }
                
                # 데이터 저장
                success_session = True
                success_error = False
                success_parts = False
                success_model_change = False
                
                # 세션 상태에 저장
                st.session_state.input_history.insert(0, session_data)  # 최신 항목이 맨 위에 오도록 추가
                
                # 정지 사유에 따른 처리
                if stop_reason == get_input_text("stop_reason_model_change", lang):
                    # 모델 변경 데이터 저장
                    model_change_data = {
                        "timestamp": timestamp_str,
                        "equipment_number": formatted_equipment,
                        "serial_number": st.session_state.serial_number,
                        "model_from": model_from,
                        "model_to": model_to,
                        "start_time": stop_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": stop_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "duration_minutes": stop_duration,
                        "details": model_change_details if 'model_change_details' in locals() else "",
                        "worker": worker,
                        "supervisor": supervisor
                    }
                    
                    try:
                        model_result = add_model_change(model_change_data)
                        if model_result:
                            success_model_change = True
                            st.success(f"모델 변경 데이터가 성공적으로 저장되었습니다.")
                    except Exception as e:
                        st.warning(f"모델 변경 데이터 저장 오류: {str(e)}")
                        
                else:
                    # 일반 정지 기록 저장
                    stop_data = {
                        "timestamp": timestamp_str,
                        "equipment_number": formatted_equipment,
                        "serial_number": st.session_state.serial_number,
                        "stop_reason": stop_reason,
                        "start_time": stop_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": stop_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "duration_minutes": stop_duration,
                        "details": error_detail,
                        "worker": worker,
                        "supervisor": supervisor
                    }
                    
                    try:
                        stop_result = add_equipment_stop(stop_data)
                        if stop_result:
                            st.success(f"정지 기록이 성공적으로 저장되었습니다.")
                    except Exception as e:
                        st.warning(f"정지 기록 저장 오류: {str(e)}")
                
                # Supabase에 저장
                try:
                    # 에러 이력 저장
                    error_result = add_error_history(error_data)
                    if error_result:
                        success_error = True
                    
                    # 부품 교체 이력 저장
                    parts_result = add_parts_replacement(parts_data)
                    if parts_result:
                        success_parts = True
                        
                    if success_error and success_parts:
                        if not success_model_change:  # 모델 변경 데이터가 이미 성공 메시지를 표시했다면 중복 표시하지 않음
                            st.success(get_input_text("save_success", lang))
                    else:
                        st.warning(get_input_text("save_session_only", lang))
                except Exception as e:
                    st.warning(f"{get_input_text('save_error', lang)}: {str(e)}")
                    st.info(get_input_text("save_session", lang))
    
    # 입력 내역 표시
    if st.session_state.input_history:
        st.subheader(get_input_text("input_history", lang))
        
        # 데이터프레임 생성
        df = pd.DataFrame(st.session_state.input_history)
        
        # 컬럼 이름 변경
        rename_dict = {
            "timestamp": get_input_text("input_time", lang),
            "equipment": get_input_text("equipment_number", lang),
            "serial_number": get_input_text("serial_number", lang),
            "error_code": get_input_text("error_code", lang),
            "error_detail": get_input_text("error_detail", lang),
            "repair_time": f"{get_input_text('repair_time', lang)} ({get_input_text('minutes', lang)})",
            "part_code": get_input_text("part_code", lang),
            "worker": get_input_text("worker", lang),
            "supervisor": get_input_text("supervisor", lang),
            "images": get_input_text("image_count", lang)
        }
        df = df.rename(columns=rename_dict)
        
        # 시각화
        st.dataframe(df)
    
    # QR 코드 스캔 기능 (모바일용)
    st.markdown("---")
    st.subheader(get_input_text("qr_scan", lang))
    st.info(get_input_text("qr_info", lang))

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