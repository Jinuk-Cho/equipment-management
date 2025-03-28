import streamlit as st
import time
from datetime import datetime, timedelta
from components.dashboard import show_dashboard
from components.equipment_detail import show_equipment_detail
from components.data_input import show_data_input
from components.reports import show_reports
from components.admin import show_admin_settings
from components.language import get_text
from utils.supabase_client import sign_in_user, sign_up_user, get_supabase, update_data

# 앱 재배포 트리거 - 2024.07.17

# Streamlit Cloud에서 환경 변수 가져오기
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin")
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your_supabase_url")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your_supabase_key")

# 페이지 설정
st.set_page_config(
    page_title="ALMUS CNC 설비 관리 시스템",
    page_icon="🏭",
    layout="wide"
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
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        .language-button {
            min-width: 100px;
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
        /* 로그인 폼 스타일 */
        .login-form {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-title {
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: #2563EB;
        }
        .login-button {
            width: 100%;
            margin-top: 1rem;
        }
        /* 사용자 정보 표시 영역 */
        .user-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-avatar {
            width: 30px;
            height: 30px;
            background-color: #2563EB;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        .user-menu {
            display: flex;
            flex-direction: column;
        }
        .user-menu a {
            cursor: pointer;
            font-size: 0.8rem;
        }
        .profile-link {
            color: #2563EB;
            text-decoration: underline;
            cursor: pointer;
        }
        .logout-button {
            color: #DC2626;
            text-decoration: underline;
            cursor: pointer;
        }
        /* 계정 생성 링크 */
        .create-account-link {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        .create-account-link a {
            color: #2563EB;
            text-decoration: underline;
            cursor: pointer;
        }
        /* 프로필 페이지 */
        .profile-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .profile-title {
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: #2563EB;
        }
        .profile-section {
            margin-bottom: 1.5rem;
        }
        .back-button {
            margin-top: 1rem;
        }
        /* 전역 스타일 */
        [data-testid="stSidebarNav"] {
            background-color: #f8f9fa;
            padding-top: 1rem;
        }
        /* 상단 타이틀 스타일 */
        .main-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1f2937;
            text-align: center;
            margin: 1rem 0;
            padding: 0.5rem;
        }
        /* 프로필 드롭다운 메뉴 스타일 */
        .profile-dropdown {
            position: relative;
            display: inline-block;
            float: right;
        }
        .profile-button {
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px;
            display: flex;
            align-items: center;
            color: #1f2937;
        }
        .profile-button:hover {
            background-color: #f3f4f6;
            border-radius: 4px;
        }
        .profile-icon {
            font-size: 24px;
            margin-right: 8px;
        }
        .dropdown-content {
            display: none;
            position: absolute;
            right: 0;
            background-color: #fff;
            min-width: 160px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            border-radius: 4px;
            z-index: 1000;
        }
        .dropdown-content a {
            color: #1f2937;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
        }
        .dropdown-content a:hover {
            background-color: #f3f4f6;
        }
        .show {
            display: block;
        }
        /* 하단 버튼 숨김 */
        .bottom-buttons {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.role = None
    st.session_state.login_time = None
    st.session_state.session_expiry = None
    st.session_state.department = None
    st.session_state.phone = None
    st.session_state.user_id = None

# 언어 설정 초기화 (기본값: 한국어)
if 'language' not in st.session_state:
    st.session_state.language = 'ko'

# 현재 페이지 설정 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# 로그인/회원가입 화면 상태
if 'auth_view' not in st.session_state:
    st.session_state.auth_view = 'login'  # 'login' 또는 'register'

# 언어 변경 함수
def set_language(lang):
    st.session_state.language = lang

# 페이지 변경 함수
def set_page(page):
    st.session_state.current_page = page

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.role = None
    st.session_state.login_time = None
    st.session_state.session_expiry = None
    st.session_state.department = None
    st.session_state.phone = None
    st.session_state.user_id = None

# 세션 만료 확인
def check_session_expiry():
    if st.session_state.logged_in and st.session_state.session_expiry:
        if datetime.now() > st.session_state.session_expiry:
            logout()
            st.warning(get_text("session_expired", st.session_state.language))

# 사용자 프로필 업데이트
def update_user_profile(user_id, name, department, phone):
    if not user_id:
        return False
    
    try:
        # Supabase users 테이블 업데이트
        update_data('users', {
            'name': name,
            'department': department,
            'phone': phone
        }, 'id', user_id)
        
        # Auth 사용자 메타데이터 업데이트
        supabase = get_supabase()
        supabase.auth.admin.update_user_by_id(user_id, {
            "user_metadata": {
                "name": name,
                "department": department,
                "phone": phone
            }
        })
        
        # 세션 상태 업데이트
        st.session_state.username = name
        st.session_state.department = department
        st.session_state.phone = phone
        
        return True
    except Exception as e:
        st.error(f"프로필 업데이트 실패: {str(e)}")
        return False

# 현재 선택된 언어와 페이지
current_lang = st.session_state.language
current_page = st.session_state.current_page

# 세션 만료 확인
check_session_expiry()

# 로그인 상태가 아닌 경우 로그인 화면 표시
if not st.session_state.logged_in:
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
        
        # 언어 선택 버튼
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            ko_clicked = st.button("한국어", key="ko_button_login", help="한국어로 변경", use_container_width=True, 
                                type="primary" if current_lang == 'ko' else "secondary")
            if ko_clicked:
                set_language('ko')
                st.rerun()
        with lang_col2:
            vi_clicked = st.button("Tiếng Việt", key="vi_button_login", help="베트남어로 변경", use_container_width=True,
                                type="primary" if current_lang == 'vi' else "secondary")
            if vi_clicked:
                set_language('vi')
                st.rerun()
        
        # 로그인/회원가입 탭
        if st.session_state.auth_view == 'login':
            # 로그인 폼
            with st.form("login_form", clear_on_submit=False):
                st.markdown(f"<h3 class='login-title'>{get_text('login', current_lang)}</h3>", unsafe_allow_html=True)
                username = st.text_input(get_text('username', current_lang), placeholder="admin")
                password = st.text_input(get_text('password', current_lang), type="password")
                submit = st.form_submit_button(get_text('login', current_lang), use_container_width=True, type="primary")
                
                if submit:
                    if not username or not password:
                        st.error(get_text('fill_all_fields', current_lang))
                    else:
                        # Supabase로 로그인 시도
                        user = sign_in_user(username, password)
                        if user:
                            # 사용자 정보를 Supabase에서 가져오기
                            if user.id == "admin-user-id":  # 하드코딩된 관리자 계정인 경우
                                st.session_state.user_id = user.id
                                st.session_state.username = "관리자"
                                st.session_state.role = "admin"
                                st.session_state.department = "관리부서"
                                st.session_state.phone = "010-0000-0000"
                                st.session_state.logged_in = True
                                st.session_state.login_time = datetime.now()
                                st.session_state.session_expiry = datetime.now() + timedelta(hours=1)
                                
                                # 로그인 페이지에서 대시보드로 이동
                                set_page('dashboard')
                                st.rerun()
                            else:
                                # 일반 사용자의 경우 기존 로직 사용
                                supabase = get_supabase()
                                # 사용자 데이터 가져오기
                                users = fetch_data('users')
                                if users:
                                    user_data = next((u for u in users if u['id'] == user.id), None)
                                    if user_data:
                                        st.session_state.logged_in = True
                                        st.session_state.username = user.user_metadata.get('name', email.split('@')[0])
                                        st.session_state.email = email
                                        st.session_state.role = user.user_metadata.get('role', 'user')
                                        st.session_state.login_time = datetime.now()
                                        st.session_state.session_expiry = datetime.now() + timedelta(hours=12)
                                        st.session_state.department = user.user_metadata.get('department', '')
                                        st.session_state.phone = user.user_metadata.get('phone', '')
                                        st.session_state.user_id = user.id
                                        
                                        # 마지막 로그인 시간 업데이트
                                        update_data('users', {'last_login': datetime.now().isoformat()}, 'id', user.id)
                                        st.rerun()
                                    else:
                                        st.error(get_text('login_failed', current_lang))
                        else:
                            st.error(get_text('login_failed', current_lang))
            
            # 계정 생성 링크
            st.markdown(f"""
                <div class="create-account-link">
                    <a onclick="document.getElementById('create_account_button').click();">
                        {get_text('create_new_account', current_lang)}
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
            # 숨겨진 버튼
            hidden_container = st.container()
            with hidden_container:
                st.markdown("<div style='display: none;'>", unsafe_allow_html=True)
                if st.button(get_text('create_new_account', current_lang), key="create_account_button"):
                    st.session_state.auth_view = 'register'
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.auth_view == 'register':
            # 회원가입 폼
            with st.form("register_form", clear_on_submit=False):
                st.markdown(f"<h3 class='login-title'>{get_text('register', current_lang)}</h3>", unsafe_allow_html=True)
                
                name = st.text_input(get_text('name', current_lang))
                email = st.text_input(get_text('email', current_lang), placeholder="user@example.com")
                department = st.text_input(get_text('department', current_lang))
                phone = st.text_input(get_text('phone', current_lang))
                password = st.text_input(get_text('password', current_lang), type="password")
                confirm_password = st.text_input(get_text('confirm_password', current_lang), type="password")
                
                submit = st.form_submit_button(get_text('register', current_lang), use_container_width=True, type="primary")
                
                if submit:
                    if not name or not email or not password or not confirm_password:
                        st.error(get_text('fill_all_fields', current_lang))
                    elif password != confirm_password:
                        st.error(get_text('password_mismatch', current_lang))
                    else:
                        # Supabase로 회원가입
                        user = sign_up_user(email, password, 'user')
                        if user:
                            # 사용자 메타데이터 추가
                            supabase = get_supabase()
                            supabase.auth.update_user({
                                "data": {
                                    "name": name,
                                    "department": department,
                                    "phone": phone
                                }
                            })
                            
                            # users 테이블에 사용자 정보 저장
                            user_data = {
                                'id': user.id,
                                'email': email,
                                'name': name,
                                'role': 'user',
                                'department': department,
                                'phone': phone,
                                'created_at': datetime.now().isoformat(),
                                'last_login': None
                            }
                            supabase.table('users').insert(user_data).execute()
                            
                            st.success(get_text('register_success', current_lang))
                            st.session_state.auth_view = 'login'
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(get_text('register_failed', current_lang))
            
            # 로그인으로 돌아가기 링크
            st.markdown(f"""
                <div class="create-account-link">
                    <a onclick="document.getElementById('back_to_login_button').click();">
                        {get_text('login', current_lang)}
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
            # 숨겨진 버튼
            hidden_login_container = st.container()
            with hidden_login_container:
                st.markdown("<div style='display: none;'>", unsafe_allow_html=True)
                if st.button(get_text('login', current_lang), key="back_to_login_button"):
                    st.session_state.auth_view = 'login'
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        # 빈 공간
        pass
else:
    # 사용자 프로필 페이지
    if current_page == 'profile':
        st.title(get_text("profile", current_lang))
        
        with st.container(border=True, height=None, class_name="profile-container"):
            st.markdown(f"<h3 class='profile-title'>{get_text('profile', current_lang)}</h3>", unsafe_allow_html=True)
            
            # 프로필 폼
            with st.form("profile_form"):
                st.text_input(get_text('email', current_lang), value=st.session_state.email, disabled=True)
                
                name = st.text_input(get_text('name', current_lang), value=st.session_state.username)
                department = st.text_input(get_text('department', current_lang), value=st.session_state.department)
                phone = st.text_input(get_text('phone', current_lang), value=st.session_state.phone)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    submit = st.form_submit_button(get_text('save', current_lang), use_container_width=True, type="primary")
                
                with col2:
                    if st.form_submit_button(get_text('cancel', current_lang), use_container_width=True):
                        set_page('dashboard')
                        st.rerun()
                
                if submit:
                    if not name:
                        st.error(get_text('fill_all_fields', current_lang))
                    else:
                        if update_user_profile(st.session_state.user_id, name, department, phone):
                            st.success(get_text('user_updated', current_lang))
                            time.sleep(1)
                            set_page('dashboard')
                            st.rerun()
            
            # 대시보드로 돌아가기 버튼
            if st.button(get_text('dashboard', current_lang), key="back_to_dashboard", use_container_width=True, class_name="back-button"):
                set_page('dashboard')
                st.rerun()
        
    else:
        # 상단 바 - 제목과 언어 선택기
        col1, col2, col3 = st.columns([1, 3, 1])

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
            # 사용자 정보 및 언어 선택
            user_col, lang_col1, lang_col2 = st.columns([2, 1, 1])
            
            with user_col:
                st.markdown(f"""
                    <div class="user-info">
                        <div class="user-avatar">{st.session_state.username[0].upper()}</div>
                        <div class="user-menu">
                            <div>{st.session_state.username} ({st.session_state.role})</div>
                            <div>
                                <span class="profile-link" onclick="document.getElementById('profile_button').click();">{get_text('profile', current_lang)}</span> | 
                                <span class="logout-button" onclick="document.getElementById('logout_button').click();">{get_text('logout', current_lang)}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 숨겨진 프로필 버튼
                profile_container = st.container()
                with profile_container:
                    st.markdown("<div style='display: none;'>", unsafe_allow_html=True)
                    if st.button(get_text('profile', current_lang), key="profile_button", help=get_text('profile', current_lang)):
                        set_page('profile')
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # 숨겨진 로그아웃 버튼
                logout_container = st.container()
                with logout_container:
                    st.markdown("<div style='display: none;'>", unsafe_allow_html=True)
                    if st.button(get_text('logout', current_lang), key="logout_button", help=get_text('logout_help', current_lang)):
                        logout()
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            with lang_col1:
                ko_clicked = st.button("한국어", key="ko_button", help="한국어로 변경", use_container_width=True, 
                                    type="primary" if current_lang == 'ko' else "secondary")
                if ko_clicked:
                    set_language('ko')
                    st.rerun()
                    
            with lang_col2:
                vi_clicked = st.button("Tiếng Việt", key="vi_button", help="베트남어로 변경", use_container_width=True,
                                    type="primary" if current_lang == 'vi' else "secondary")
                if vi_clicked:
                    set_language('vi')
                    st.rerun()

        # 메뉴 바 - JavaScript 클릭 이벤트 제거하고 직접 버튼으로 구현
        menu_cols = st.columns(5)
        with menu_cols[0]:
            if st.button(get_text("dashboard", current_lang), key="menu_dashboard", 
                        type="primary" if current_page == 'dashboard' else "secondary", use_container_width=True):
                set_page('dashboard')
                st.rerun()

        with menu_cols[1]:
            if st.button(get_text("equipment_detail", current_lang), key="menu_equipment", 
                        type="primary" if current_page == 'equipment_detail' else "secondary", use_container_width=True):
                set_page('equipment_detail')
                st.rerun()

        with menu_cols[2]:
            if st.button(get_text("data_input", current_lang), key="menu_data_input", 
                        type="primary" if current_page == 'data_input' else "secondary", use_container_width=True):
                set_page('data_input')
                st.rerun()

        with menu_cols[3]:
            if st.button(get_text("reports", current_lang), key="menu_reports", 
                        type="primary" if current_page == 'reports' else "secondary", use_container_width=True):
                set_page('reports')
                st.rerun()

        with menu_cols[4]:
            if st.button(get_text("admin_settings", current_lang), key="menu_admin", 
                        type="primary" if current_page == 'admin_settings' else "secondary", use_container_width=True):
                set_page('admin_settings')
                st.rerun()

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