import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json

def show_data_input():
    """데이터 입력 페이지를 표시합니다."""
    st.title("Nhập dữ liệu / 데이터 입력")
    
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
            equipment = st.selectbox("Số thiết bị / 설비 번호", equipment_list)
            error_code = st.selectbox("Mã lỗi / 오류 코드", error_codes)
            error_detail = st.text_area("Chi tiết lỗi / 오류 상세 내용")
            repair_time = st.number_input("Thời gian sửa chữa (phút) / 수리 시간 (분)", min_value=1, max_value=480)
        
        with col2:
            part_code = st.selectbox("Mã linh kiện / 부품 코드", parts_list)
            worker = st.text_input("Người thực hiện / 작업자")
            supervisor = st.text_input("Người giám sát / 감독자")
        
        # 이미지 업로드
        st.subheader("Hình ảnh liên quan / 관련 이미지")
        uploaded_files = st.file_uploader(
            "Chọn file hình ảnh (tối đa 10 file) / 이미지 파일 선택 (최대 10개)",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True
        )
        
        # 이미지 미리보기
        if uploaded_files:
            st.subheader("Xem trước hình ảnh / 이미지 미리보기")
            cols = st.columns(5)
            for idx, file in enumerate(uploaded_files[:10]):
                with cols[idx % 5]:
                    st.image(file, use_column_width=True)
                    st.caption(f"Hình ảnh / 이미지 {idx + 1}")
        
        submitted = st.form_submit_button("Lưu / 저장")
        
        if submitted:
            if not all([equipment, error_code, error_detail, repair_time, worker, supervisor]):
                st.error("Vui lòng điền vào tất cả các trường / 모든 필드를 입력해주세요.")
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
                data = {
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "equipment": equipment,
                    "error_code": error_code,
                    "error_detail": error_detail,
                    "repair_time": repair_time,
                    "part_code": part_code,
                    "worker": worker,
                    "supervisor": supervisor,
                    "images": len(image_paths)
                }
                
                # 입력 내역에 추가
                st.session_state.input_history.insert(0, data)  # 최신 항목이 맨 위에 오도록 추가
                
                st.success("Dữ liệu đã được lưu thành công / 데이터가 저장되었습니다.")
    
    # 입력 내역 표시
    if st.session_state.input_history:
        st.subheader("Lịch sử nhập dữ liệu / 입력 내역")
        
        # 데이터프레임 생성
        df = pd.DataFrame(st.session_state.input_history)
        
        # 컬럼명 지정
        df = df.rename(columns={
            "timestamp": "Thời gian nhập / 입력 시간",
            "equipment": "Số thiết bị / 설비 번호", 
            "error_code": "Mã lỗi / 오류 코드",
            "error_detail": "Chi tiết lỗi / 오류 상세",
            "repair_time": "Thời gian sửa chữa / 수리 시간",
            "part_code": "Mã linh kiện / 부품 코드",
            "worker": "Người thực hiện / 작업자",
            "supervisor": "Người giám sát / 감독자",
            "images": "Số lượng hình ảnh / 이미지 수량"
        })
        
        # repair_time 칼럼에 '분' 단위 추가
        df["Thời gian sửa chữa / 수리 시간"] = df["Thời gian sửa chữa / 수리 시간"].astype(str) + " phút / 분"
        
        # 스타일을 적용한 테이블로 표시
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    
    # QR 코드 스캔 기능 (모바일용)
    st.markdown("---")
    st.subheader("Quét mã QR / QR 코드 스캔")
    st.info("Khi quét mã QR trên thiết bị di động, thông tin thiết bị sẽ được tự động điền / 모바일에서 QR 코드를 스캔하면 자동으로 설비 정보가 입력됩니다.") 