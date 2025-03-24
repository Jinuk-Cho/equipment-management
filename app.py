import streamlit as st
import time
from datetime import datetime, timedelta
from components.dashboard import show_dashboard
from components.equipment_detail import show_equipment_detail
from components.data_input import show_data_input
from components.reports import show_reports
from components.admin import show_admin_settings

# Streamlit Cloud에서 환경 변수 가져오기
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin")

# 페이지 설정
st.set_page_config(
    page_title="Hệ thống quản lý thiết bị / 설비 관리 시스템",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
    <style>
        .main > div {
            max-width: 1200px;
            margin: auto;
            padding-top: 1rem;
        }
        .stButton>button {
            width: 100%;
        }
        /* 사이드바 스타일 */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            min-width: 200px !important;
            max-width: 250px !important;
        }
        /* 메인 컨텐츠 영역 */
        .main .block-container {
            padding-left: 20px;
            padding-right: 20px;
        }
        /* 제목 스타일 */
        .system-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        .system-title-vn {
            color: #1E3A8A;
            margin-bottom: 0.3rem;
        }
        .system-title-kr {
            color: #2563EB;
        }
        /* 메뉴 스타일 */
        .menu-item {
            font-size: 0.9rem;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }
        .menu-item-vn {
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .menu-item-kr {
            color: #2563EB;
        }
        /* 라벨 스타일 */
        .label-text {
            font-size: 0.9rem;
            line-height: 1.2;
        }
        .label-text-vn {
            color: #1E3A8A;
        }
        .label-text-kr {
            color: #2563EB;
            margin-left: 0.3rem;
        }
        /* 메뉴 탭 스타일 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 1rem;
            font-weight: bold;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e2e8f0;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #2563EB;
        }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'login_time' not in st.session_state:
    st.session_state.login_time = None
if 'session_expiry' not in st.session_state:
    st.session_state.session_expiry = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"

# 세션 만료 체크 (12시간)
def check_session_expiry():
    if st.session_state.logged_in and st.session_state.session_expiry:
        if datetime.now() > st.session_state.session_expiry:
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.login_time = None
            st.session_state.session_expiry = None
            st.rerun()

# 세션 체크
check_session_expiry()

# 로그인 페이지
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div class="system-title">
                <div class="system-title-vn">Hệ thống quản lý thiết bị</div>
                <div class="system-title-kr">설비 관리 시스템</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # 로그인 폼
        st.markdown("""
            <div class="menu-item">
                <div class="menu-item-vn">Đăng nhập</div>
                <div class="menu-item-kr">로그인</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("""
                <div class="label-text">
                    <span class="label-text-vn">ID</span>
                    <span class="label-text-kr">아이디</span>
                </div>
            """, unsafe_allow_html=True)
            username = st.text_input("username_label", label_visibility="collapsed", key="username_input")
            
            st.markdown("""
                <div class="label-text">
                    <span class="label-text-vn">Mật khẩu</span>
                    <span class="label-text-kr">비밀번호</span>
                </div>
            """, unsafe_allow_html=True)
            password = st.text_input("password_label", type="password", label_visibility="collapsed", key="password_input")
            
            submit = st.form_submit_button("Đăng nhập / 로그인", use_container_width=True)
            
            if submit:
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = "admin"
                    st.session_state.login_time = datetime.now()
                    st.session_state.session_expiry = datetime.now() + timedelta(hours=12)
                    st.success("Đăng nhập thành công! / 로그인 성공!")
                    st.rerun()
                else:
                    st.error("ID hoặc mật khẩu không chính xác / 아이디 또는 비밀번호가 일치하지 않습니다.")

# 메인 애플리케이션
else:
    # 사이드바 - 최소화된 사용자 정보만 표시
    with st.sidebar:
        st.markdown("""
            <div class="system-title">
                <div class="system-title-vn">Xin chào!</div>
                <div class="system-title-kr">환영합니다!</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="label-text">
                <span class="label-text-vn">Người dùng</span>
                <span class="label-text-kr">사용자</span>: {st.session_state.username}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="label-text">
                <span class="label-text-vn">Thời gian đăng nhập</span>
                <span class="label-text-kr">로그인 시간</span>: {st.session_state.login_time.strftime('%Y-%m-%d %H:%M')}
            </div>
        """, unsafe_allow_html=True)
        
        remaining_time = st.session_state.session_expiry - datetime.now()
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        st.markdown(f"""
            <div class="label-text">
                <span class="label-text-vn">Thời gian còn lại</span>
                <span class="label-text-kr">세션 만료까지</span>: {hours}시간 {minutes}분
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Đăng xuất / 로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.login_time = None
            st.session_state.session_expiry = None
            st.rerun()
    
    # 메인 컨텐츠 영역 - 상단에 메뉴 탭 표시
    st.markdown("""
        <div class="system-title">
            <div class="system-title-vn">Hệ thống quản lý thiết bị</div>
            <div class="system-title-kr">설비 관리 시스템</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 탭 메뉴를 메인 컨텐츠의 최상단에 명확하게 표시
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Bảng điều khiển / 대시보드",
        "Chi tiết thiết bị / 설비 상세",
        "Nhập dữ liệu / 데이터 입력",
        "Báo cáo / 보고서",
        "Cài đặt quản trị / 관리자 설정"
    ])
    
    # 각 탭의 컨텐츠
    with tab1:
        show_dashboard()
    with tab2:
        show_equipment_detail()
    with tab3:
        show_data_input()
    with tab4:
        show_reports()
    with tab5:
        if st.session_state.role == 'admin':
            show_admin_settings()
        else:
            st.error("Yêu cầu quyền quản trị viên / 관리자 권한이 필요합니다.")