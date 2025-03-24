import streamlit as st
import time
from datetime import datetime, timedelta
from components.dashboard import show_dashboard
from components.equipment_detail import show_equipment_detail
from components.data_input import show_data_input
from components.reports import show_reports
from components.admin import show_admin_settings
from components.language import get_text

# 앱 재배포 트리거 - 2024.07.17

# Streamlit Cloud에서 환경 변수 가져오기
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin")

# 페이지 설정
st.set_page_config(
    page_title="설비 관리 시스템 | Hệ thống quản lý thiết bị",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
st.markdown("""
    <style>
        .main > div {
            padding: 0 !important;
        }
        .stButton>button {
            width: 100%;
        }
        /* 메인 컨텐츠 영역 */
        .main .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        /* 제목 스타일 */
        .system-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            line-height: 1.2;
            text-align: center;
        }
        .system-title-vn {
            color: #1E3A8A;
            margin-bottom: 0.3rem;
        }
        .system-title-kr {
            color: #2563EB;
        }
        /* 차트 컨테이너 */
        .chart-container {
            margin-bottom: 1rem;
        }
        /* 플롯리 차트 크기 조정 */
        .js-plotly-plot {
            height: 300px !important;
        }
        /* 언어 선택 버튼 */
        .language-selector {
            width: 120px;
        }
        /* 메뉴 바 */
        .menu-bar {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }
        .menu-item {
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .menu-item:hover {
            background-color: #e9ecef;
        }
        .menu-item.active {
            background-color: #2563EB;
            color: white;
        }
        /* 상단 바 */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        /* 언어 선택기 컨테이너 */
        .language-container {
            display: flex;
            justify-content: flex-end;
        }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.username = "admin"
    st.session_state.role = "admin"
    st.session_state.login_time = datetime.now()
    st.session_state.session_expiry = datetime.now() + timedelta(hours=12)

# 언어 설정 초기화 (기본값: 한국어)
if 'language' not in st.session_state:
    st.session_state.language = 'ko'

# 현재 페이지 설정 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

def toggle_language():
    """언어 설정을 변경합니다."""
    if st.session_state.language == 'ko':
        st.session_state.language = 'vi'
    else:
        st.session_state.language = 'ko'
    st.rerun()

def change_page(page):
    """페이지를 변경합니다."""
    st.session_state.current_page = page
    st.rerun()

# 현재 선택된 언어
current_lang = st.session_state.language
current_page = st.session_state.current_page

# 상단 바 - 제목과 언어 선택기
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    # 빈 공간
    pass

with col2:
    # 시스템 제목
    st.markdown(f"""
        <div class="system-title">
            {get_text("system_title", current_lang)}
        </div>
    """, unsafe_allow_html=True)

with col3:
    # 언어 선택 버튼
    language_display = "한국어" if current_lang == 'ko' else "Tiếng Việt"
    st.button(language_display, key="language_button", on_click=toggle_language, help="언어 변경 / Thay đổi ngôn ngữ", use_container_width=True)

# 메뉴 바
st.markdown(f"""
    <div class="menu-bar">
        <div class="menu-item {'active' if current_page == 'dashboard' else ''}" 
             onclick="parent.postMessage({{command: 'streamlitClick', target: 'dashboard_btn'}}, '*')">
            {get_text("dashboard", current_lang)}
        </div>
        <div class="menu-item {'active' if current_page == 'equipment_detail' else ''}" 
             onclick="parent.postMessage({{command: 'streamlitClick', target: 'equipment_btn'}}, '*')">
            {get_text("equipment_detail", current_lang)}
        </div>
        <div class="menu-item {'active' if current_page == 'data_input' else ''}" 
             onclick="parent.postMessage({{command: 'streamlitClick', target: 'data_input_btn'}}, '*')">
            {get_text("data_input", current_lang)}
        </div>
        <div class="menu-item {'active' if current_page == 'reports' else ''}" 
             onclick="parent.postMessage({{command: 'streamlitClick', target: 'reports_btn'}}, '*')">
            {get_text("reports", current_lang)}
        </div>
        <div class="menu-item {'active' if current_page == 'admin_settings' else ''}" 
             onclick="parent.postMessage({{command: 'streamlitClick', target: 'admin_btn'}}, '*')">
            {get_text("admin_settings", current_lang)}
        </div>
    </div>
""", unsafe_allow_html=True)

# 숨겨진 버튼으로 JavaScript 클릭 이벤트 처리
if st.button("대시보드", key="dashboard_btn", on_click=change_page, args=('dashboard',), help="대시보드로 이동", visible=False):
    pass
if st.button("설비 상세", key="equipment_btn", on_click=change_page, args=('equipment_detail',), help="설비 상세로 이동", visible=False):
    pass
if st.button("데이터 입력", key="data_input_btn", on_click=change_page, args=('data_input',), help="데이터 입력으로 이동", visible=False):
    pass
if st.button("보고서", key="reports_btn", on_click=change_page, args=('reports',), help="보고서로 이동", visible=False):
    pass
if st.button("관리자 설정", key="admin_btn", on_click=change_page, args=('admin_settings',), help="관리자 설정으로 이동", visible=False):
    pass

# 컨텐츠 표시
if current_page == 'dashboard':
    show_dashboard(current_lang)
elif current_page == 'equipment_detail':
    show_equipment_detail(current_lang)
elif current_page == 'data_input':
    show_data_input(current_lang)
elif current_page == 'reports':
    show_reports(current_lang)
elif current_page == 'admin_settings':
    if st.session_state.role == 'admin':
        show_admin_settings(current_lang)
    else:
        st.error(get_text("admin_required", current_lang))