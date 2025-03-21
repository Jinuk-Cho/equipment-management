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
    initial_sidebar_state="collapsed"
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
        
        tabs = st.tabs(["로그인", "회원가입"])
        
        with tabs[0]:
            st.subheader("로그인")
            email = st.text_input("이메일", key="login_email")
            password = st.text_input("비밀번호", type="password", key="login_password")
            st.markdown("---")
            if st.button("로그인", key="login_button", use_container_width=True):
                if email and password:  # 입력값 검증
                    if email == "admin@example.com" and password == "admin123456":
                        st.session_state.user = {"email": email, "role": "admin"}
                        st.success("로그인 성공!")
                        st.rerun()
                    else:
                        user = sign_in_user(email, password)
                        if user:
                            st.session_state.user = user
                            st.success("로그인 성공!")
                            st.rerun()
                else:
                    st.error("이메일과 비밀번호를 입력해주세요.")
        
        with tabs[1]:
            st.subheader("회원가입")
            new_email = st.text_input("이메일", key="signup_email")
            new_password = st.text_input("비밀번호", type="password", key="signup_password")
            confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
            st.markdown("---")
            if st.button("회원가입", key="signup_button", use_container_width=True):
                if new_email and new_password and confirm_password:  # 입력값 검증
                    if len(new_password) < 6:
                        st.error("비밀번호는 6자 이상이어야 합니다.")
                    elif new_password != confirm_password:
                        st.error("비밀번호가 일치하지 않습니다.")
                    else:
                        user = sign_up_user(new_email, new_password)
                        if user:
                            st.success("회원가입 성공! 로그인해주세요.")
                else:
                    st.error("모든 필드를 입력해주세요.")

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