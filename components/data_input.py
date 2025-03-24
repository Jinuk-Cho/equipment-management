import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from utils.supabase_client import add_error_history, add_parts_replacement
from components.language import get_text

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
    }
}

def get_input_text(key, lang):
    """데이터 입력 페이지 전용 텍스트를 가져옵니다."""
    if key in DATA_INPUT_TEXTS:
        return DATA_INPUT_TEXTS[key].get(lang, DATA_INPUT_TEXTS[key]['ko'])
    return f"[{key}]"

def show_data_input(lang='ko'):
    """데이터 입력 페이지를 표시합니다."""
    st.title(get_input_text("data_input", lang))
    
    # 세션 상태에 입력 내역 저장하기 위한 초기화
    if 'input_history' not in st.session_state:
        st.session_state.input_history = []
    
    # 예시 데이터
    equipment_list = ['EQ001', 'EQ002', 'EQ003', 'EQ004']
    error_codes = ['E001', 'E002', 'E003', 'E004', 'E005']
    parts_list = ['P001', 'P002', 'P003', 'P004']
    
    # 입력 폼
    with st.form("data_input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            equipment = st.selectbox(get_input_text("equipment_number", lang), equipment_list)
            error_code = st.selectbox(get_input_text("error_code", lang), error_codes)
            error_detail = st.text_area(get_input_text("error_detail", lang))
            repair_time = st.number_input(get_input_text("repair_time", lang), min_value=1, max_value=480)
        
        with col2:
            part_code = st.selectbox(get_input_text("part_code", lang), parts_list)
            worker = st.text_input(get_input_text("worker", lang))
            supervisor = st.text_input(get_input_text("supervisor", lang))
        
        # 이미지 업로드
        st.subheader(get_input_text("related_images", lang))
        uploaded_files = st.file_uploader(
            get_input_text("select_images", lang),
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True
        )
        
        # 이미지 미리보기
        if uploaded_files:
            st.subheader(get_input_text("image_preview", lang))
            cols = st.columns(5)
            for idx, file in enumerate(uploaded_files[:10]):
                with cols[idx % 5]:
                    st.image(file, use_column_width=True)
                    st.caption(f"{get_input_text('image', lang)} {idx + 1}")
        
        submitted = st.form_submit_button(get_input_text("save", lang))
        
        if submitted:
            if not all([equipment, error_code, error_detail, repair_time, worker, supervisor]):
                st.error(get_input_text("fill_all_fields", lang))
            else:
                # 이미지 저장
                image_paths = []
                if uploaded_files:
                    save_dir = f"uploads/{datetime.now().strftime('%Y%m%d')}"
                    os.makedirs(save_dir, exist_ok=True)
                    
                    for idx, file in enumerate(uploaded_files[:10]):
                        file_path = os.path.join(save_dir, f"{equipment}_{datetime.now().strftime('%H%M%S')}_{idx+1}{os.path.splitext(file.name)[1]}")
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        image_paths.append(file_path)
                
                # 입력 데이터 생성
                timestamp = datetime.now()
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # 세션용 데이터
                session_data = {
                    "timestamp": timestamp_str,
                    "equipment": equipment,
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
                    "equipment_number": equipment,
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
                    "equipment_number": equipment,
                    "part_code": part_code,
                    "worker": worker,
                    "supervisor": supervisor
                }
                
                # 데이터 저장
                success_session = True
                success_error = False
                success_parts = False
                
                # 세션 상태에 저장
                st.session_state.input_history.insert(0, session_data)  # 최신 항목이 맨 위에 오도록 추가
                
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
        
        # 칼럼명 번역
        column_names = {
            "timestamp": get_input_text("input_time", lang),
            "equipment": get_input_text("equipment_number", lang), 
            "error_code": get_input_text("error_code", lang),
            "error_detail": get_input_text("error_detail", lang),
            "repair_time": get_input_text("repair_time", lang),
            "part_code": get_input_text("part_code", lang),
            "worker": get_input_text("worker", lang),
            "supervisor": get_input_text("supervisor", lang),
            "images": get_input_text("image_count", lang)
        }
        
        # 컬럼명 지정
        df = df.rename(columns=column_names)
        
        # repair_time 칼럼에 '분' 단위 추가
        minutes_text = get_input_text("minutes", lang)
        df[get_input_text("repair_time", lang)] = df[get_input_text("repair_time", lang)].astype(str) + f" {minutes_text}"
        
        # 스타일을 적용한 테이블로 표시
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    
    # QR 코드 스캔 기능 (모바일용)
    st.markdown("---")
    st.subheader(get_input_text("qr_scan", lang))
    st.info(get_input_text("qr_info", lang)) 