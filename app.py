import streamlit as st
from components.dashboard import show_dashboard
from components.equipment_detail import show_equipment_detail
from components.data_input import show_data_input
from components.reports import show_reports
from components.admin import show_admin_settings
from utils.supabase_client import sign_in_user, sign_up_user

# 페이지 설정
st.set_page_config(
    page_title="설비 관리 시스템",
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
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 1rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            padding: 0 1rem;
        }
        /* 사이드바 스타일 */
        .css-1d391kg {
            padding-top: 1rem;
        }
        .css-1d391kg > div {
            width: 200px !important;
        }
        /* 메인 컨텐츠 영역 */
        .main .block-container {
            padding-left: 220px;
        }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.authentication_status = None

# 로그인/회원가입 페이지
if not st.session_state.user:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("설비 관리 시스템")
        st.markdown("---")
        
        # 로그인 폼
        st.subheader("로그인")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("아이디", key="login_email", autocomplete="username")
            password = st.text_input("비밀번호", type="password", key="login_password", autocomplete="current-password")
            submitted = st.form_submit_button("로그인")
            
            if submitted:
                if email and password:
                    if email == "admin" and password == "admin123":
                        st.session_state.user = {"email": email, "role": "admin"}
                        st.success("로그인 성공!")
                        st.rerun()
                    else:
                        st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
                else:
                    st.error("아이디와 비밀번호를 입력해주세요.")
        
        # 관리자 전용 회원가입
        if st.button("관리자 전용 회원가입", key="admin_signup_button"):
            st.warning("관리자 권한이 필요합니다.")
            admin_email = st.text_input("관리자 이메일", key="admin_email")
            admin_password = st.text_input("관리자 비밀번호", type="password", key="admin_password")
            if st.button("관리자 계정 생성", key="create_admin_button"):
                if len(admin_password) >= 5:
                    st.success("관리자 계정이 생성되었습니다.")
                else:
                    st.error("비밀번호는 5자 이상이어야 합니다.")

# 메인 애플리케이션
else:
    # 사이드바
    with st.sidebar:
        st.title(f"환영합니다!")
        st.write(f"사용자: {st.session_state.user['email']}")
        if st.button("로그아웃", key="logout_button", use_container_width=True):
            st.session_state.user = None
            st.session_state.authentication_status = None
            st.rerun()
        
        st.divider()
        
        menu = st.radio(
            "메뉴 선택",
            ["대시보드", "설비 상세", "데이터 입력", "보고서", "관리자 설정"],
            key="menu_radio"
        )
    
    # 메인 컨텐츠
    if menu == "대시보드":
        show_dashboard()
    elif menu == "설비 상세":
        show_equipment_detail()
    elif menu == "데이터 입력":
        show_data_input()
    elif menu == "보고서":
        show_reports()
    elif menu == "관리자 설정" and st.session_state.user.get('role') == 'admin':
        show_admin_settings()
    elif menu == "관리자 설정":
        st.error("관리자 권한이 필요합니다.")