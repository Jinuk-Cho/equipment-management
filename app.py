import streamlit as st
import traceback
import sys

# 개발 모드 설정 (True: 자동 로그인, False: 일반 로그인)
DEV_MODE = True

# 페이지 설정
st.set_page_config(
    page_title="설비 관리 시스템 | Hệ thống quản lý thiết bị",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전역 예외 처리
try:
    import time
    from datetime import datetime, timedelta
    from components.language import get_text, set_language
    from utils.supabase_client import sign_in_user, sign_up_user, get_supabase, update_data

    # 필요한 컴포넌트만 import
    from components.dashboard import DashboardComponent
    from components.equipment_detail import EquipmentDetailComponent
    from components.data_input import DataInputComponent
    from components.reports import ReportsComponent
    from components.admin import AdminComponent
    from components.plan_suspension import PlanSuspensionComponent
    from components.plan_management import PlanManagementComponent
    from components.equipment_status_detail import EquipmentStatusDetailComponent
except Exception as e:
    st.error(f"앱 초기화 중 오류가 발생했습니다: {str(e)}")
    st.code(traceback.format_exc())

# 앱 재배포 트리거 - 2024.07.19

# Streamlit Cloud에서 환경 변수 가져오기
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin")
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your_supabase_url")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your_supabase_key")

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
        h1.system-title {
            margin-top: 0;
            margin-bottom: 0.5rem;
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
        /* 데이터 테이블 스타일 */
        .dataframe {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        .dataframe th {
            background-color: #f1f5f9;
            padding: 0.5rem;
            text-align: left;
            border: 1px solid #e5e7eb;
        }
        .dataframe td {
            padding: 0.5rem;
            border: 1px solid #e5e7eb;
        }
        /* 모바일 최적화 */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem !important;
            }
            .system-title {
                font-size: 1.2rem;
            }
            .user-menu a {
                font-size: 0.7rem;
            }
        }
        /* 버튼 상태 스타일 */
        .stButton>button:active {
            transform: translateY(1px);
        }
        /* 스크롤바 스타일 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        /* 입력 필드 포커스 효과 */
        input:focus, textarea:focus, select:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'user' not in st.session_state:
    st.session_state.user = None

if 'role' not in st.session_state:
    st.session_state.role = None

if 'auth_view' not in st.session_state:
    st.session_state.auth_view = 'login'

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'ko'  # 기본 언어를 'ko'로 설정

if 'last_activity' not in st.session_state:
    st.session_state.last_activity = datetime.now()

# 기타 함수들
def set_page(page_name):
    st.session_state.current_page = page_name

def check_session_expiry():
    # 30분 세션 제한
    if datetime.now() - st.session_state.last_activity > timedelta(minutes=30):
        return False
    st.session_state.last_activity = datetime.now()
    return True

def logout():
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.current_page = 'dashboard'
    st.rerun()

def update_user_profile(user_id, name, department, phone):
    try:
        # 스토어 또는 API를 이용해 사용자 프로필 업데이트
        # 여기서는 예제로 항상 성공으로 가정
        update_data('users', user_id, {'name': name, 'department': department, 'phone': phone})
        return True
    except Exception as e:
        print(f"Profile update error: {str(e)}")
        return False

# 언어 선택 초기화
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'ko'  # 기본 언어를 'ko'로 설정

# 호환성을 위한 언어 코드 변환
current_lang = st.session_state.current_lang
if current_lang == 'kr':
    current_lang = 'ko'
elif current_lang == 'vn':
    current_lang = 'vi'

# 컴포넌트 초기화 - 표준화된 언어 코드 사용
dashboard_component = DashboardComponent(lang=current_lang)
equipment_detail_component = EquipmentDetailComponent(lang=current_lang)
data_input_component = DataInputComponent(lang=current_lang)
reports_component = ReportsComponent(lang=current_lang)
admin_component = AdminComponent(lang=current_lang)
plan_management_component = PlanManagementComponent(lang=current_lang)
plan_suspension_component = PlanSuspensionComponent(lang=current_lang)
equipment_status_detail_component = EquipmentStatusDetailComponent(lang=current_lang)

# 상단 헤더
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"""
        <div>
            <h1 class="system-title system-title-vn">Hệ thống quản lý thiết bị</h1>
            <h1 class="system-title system-title-kr">설비 관리 시스템</h1>
        </div>
    """, unsafe_allow_html=True)

# 언어 선택
lang_col1, lang_col2 = st.columns([9, 1])
with lang_col2:
    selected_lang = st.radio("", ["한국어", "Tiếng Việt"], index=0 if current_lang == 'ko' else 1, horizontal=True, label_visibility="collapsed")
    
    if (selected_lang == "한국어" and current_lang != 'ko') or (selected_lang == "Tiếng Việt" and current_lang != 'vi'):
        if selected_lang == "한국어":
            st.session_state.current_lang = 'ko'
        else:
            st.session_state.current_lang = 'vi'
        st.rerun()

# 개발 모드 자동 로그인 처리
if DEV_MODE and not st.session_state.user:
    st.session_state.user = {
        'email': 'admin',
        'name': 'admin'
    }
    st.session_state.role = 'admin'

# 인증 상태 확인
if not st.session_state.user:
    # 로그인 화면 표시
    if st.session_state.auth_view == 'login':
        with st.container():
            st.markdown(f"""<h2 class="login-title">{get_text('login_title', current_lang)}</h2>""", unsafe_allow_html=True)
            
            email = st.text_input(get_text("email", current_lang))
            password = st.text_input(get_text("password", current_lang), type="password")
            
            login_col1, login_col2 = st.columns(2)
            
            with login_col1:
                if st.button(get_text("login", current_lang), type="primary", use_container_width=True):
                    if not email or not password:
                        st.error(get_text("fill_all_fields", current_lang))
                    else:
                        # 관리자 로그인 처리
                        if email == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                            st.session_state.user = {
                                'email': email,
                                'name': 'Administrator',
                                'role': 'admin'
                            }
                            st.session_state.role = 'admin'
                            st.rerun()
                        else:
                            # 일반 사용자 로그인 처리
                            try:
                                user_data = sign_in_user(email, password)
                                if user_data:
                                    st.session_state.user = user_data
                                    st.session_state.role = user_data.get('role', 'user')
                                    st.rerun()
                                else:
                                    st.error(get_text("invalid_credentials", current_lang))
                            except Exception as e:
                                st.error(f"{get_text('login_error', current_lang)}: {str(e)}")
            
            with login_col2:
                if st.button(get_text("demo_login", current_lang), type="secondary", use_container_width=True):
                    # 데모 계정으로 로그인
                    st.session_state.user = {
                        'email': 'demo@example.com',
                        'name': 'Demo User',
                        'role': 'user'
                    }
                    st.session_state.role = 'user'
                    st.rerun()
            
            # 회원가입 링크
            st.markdown(
                f"""
                <div class="create-account-link">
                    <span>{get_text('no_account', current_lang)}</span>
                    <a href="#" onclick="setTimeout(function(){{window.location.reload()}}, 100)">{get_text('create_account', current_lang)}</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # 회원가입 링크 처리 - style 파라미터 제거
            if False:  # 숨김 처리를 위해 조건을 False로 설정
                if st.button(get_text("create_account", current_lang), key="create_account_btn"):
                    st.session_state.auth_view = 'register'
                    st.rerun()
    else:
        # 회원가입 화면
        with st.container():
            st.markdown(f"""<h2 class="login-title">{get_text('register_title', current_lang)}</h2>""", unsafe_allow_html=True)
            
            reg_col1, reg_col2 = st.columns(2)
            
            with reg_col1:
                reg_name = st.text_input(get_text("name", current_lang))
                reg_email = st.text_input(get_text("email", current_lang))
                reg_password = st.text_input(get_text("password", current_lang), type="password")
            
            with reg_col2:
                reg_department = st.text_input(get_text("department", current_lang))
                reg_phone = st.text_input(get_text("phone", current_lang))
                reg_password_confirm = st.text_input(get_text("confirm_password", current_lang), type="password")
            
            reg_btn_col1, reg_btn_col2 = st.columns(2)
            
            with reg_btn_col1:
                if st.button(get_text("register", current_lang), type="primary", use_container_width=True):
                    if not all([reg_name, reg_email, reg_password, reg_password_confirm]):
                        st.error(get_text("fill_required_fields", current_lang))
                    elif reg_password != reg_password_confirm:
                        st.error(get_text("password_mismatch", current_lang))
                    else:
                        try:
                            user_data = sign_up_user(reg_email, reg_password, {
                                'name': reg_name,
                                'department': reg_department,
                                'phone': reg_phone,
                                'role': 'user'
                            })
                            
                            if user_data:
                                st.success(get_text("registration_success", current_lang))
                                time.sleep(2)
                                st.session_state.auth_view = 'login'
                                st.rerun()
                            else:
                                st.error(get_text("registration_error", current_lang))
                        except Exception as e:
                            st.error(f"{get_text('registration_error', current_lang)}: {str(e)}")
            
            with reg_btn_col2:
                if st.button(get_text("back_to_login", current_lang), type="secondary", use_container_width=True):
                    st.session_state.auth_view = 'login'
                    st.rerun()
else:
    # 인증된 사용자만 접근 가능한 영역
    # 세션 만료 확인
    if not check_session_expiry():
        st.warning(get_text("session_expired", current_lang))
        st.session_state.user = None
        st.rerun()
    
    # 프로필 페이지 표시
    if st.session_state.current_page == 'profile':
        st.subheader(get_text("profile_title", current_lang))
        
        with st.container():
            profile_col1, profile_col2 = st.columns(2)
            
            with profile_col1:
                name = st.text_input(get_text("name", current_lang), value=st.session_state.user.get('name', ''))
                department = st.text_input(get_text("department", current_lang), value=st.session_state.user.get('department', ''))
            
            with profile_col2:
                email = st.text_input(get_text("email", current_lang), value=st.session_state.user.get('email', ''), disabled=True)
                phone = st.text_input(get_text("phone", current_lang), value=st.session_state.user.get('phone', ''))
            
            if st.button(get_text("save_profile", current_lang)):
                if update_user_profile(st.session_state.user['id'], name, department, phone):
                    st.success(get_text("profile_updated", current_lang))
                    st.session_state.user['name'] = name
                    st.session_state.user['department'] = department
                    st.session_state.user['phone'] = phone
                else:
                    st.error(get_text("profile_update_error", current_lang))
            
            if st.button(get_text("back", current_lang)):
                set_page('dashboard')
                st.rerun()
    else:
        # 사용자 정보 표시 (로그인 상태)
        with col2:
            st.markdown(
                f"""
                <div class="user-info">
                    <div class="user-avatar">{st.session_state.user.get('name', 'U')[0]}</div>
                    <div class="user-menu">
                        <span>{st.session_state.user.get('name', get_text('user', current_lang))}</span>
                        <span>
                            <a class="profile-link" href="#" onclick="setTimeout(function(){{window.location.reload()}}, 100)">{get_text('profile', current_lang)}</a> |
                            <a class="logout-button" href="#" onclick="setTimeout(function(){{window.location.reload()}}, 100)">{get_text('logout', current_lang)}</a>
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # 프로필 링크 처리 - style 파라미터 제거
        if False:  # 숨김 처리를 위해 조건을 False로 설정
            if st.button(get_text('profile', current_lang), key="profile_btn", type="secondary"):
                set_page('profile')
                st.rerun()
            
        # 로그아웃 버튼 처리 - style 파라미터 제거
        if False:  # 숨김 처리를 위해 조건을 False로 설정
            if st.button(get_text('logout', current_lang), key="logout_btn", type="secondary"):
                logout()
        
        # 메뉴 바
        menu_cols = st.columns(5)
        
        with menu_cols[0]:
            if st.button(get_text("dashboard", current_lang), key="menu_dashboard", 
                        type="primary" if st.session_state.current_page == 'dashboard' else "secondary", use_container_width=True):
                set_page('dashboard')
                st.rerun()
                
        with menu_cols[1]:
            if st.button(get_text("equipment_detail", current_lang), key="menu_equipment", 
                        type="primary" if st.session_state.current_page == 'equipment_detail' else "secondary", use_container_width=True):
                set_page('equipment_detail')
                st.rerun()
                
        with menu_cols[2]:
            if st.button(get_text("data_input", current_lang), key="menu_data_input", 
                        type="primary" if st.session_state.current_page == 'data_input' else "secondary", use_container_width=True):
                set_page('data_input')
                st.rerun()
                
        with menu_cols[3]:
            if st.button(get_text("reports", current_lang), key="menu_reports", 
                        type="primary" if st.session_state.current_page == 'reports' else "secondary", use_container_width=True):
                set_page('reports')
                st.rerun()
                
        with menu_cols[4]:
            if st.button(get_text("plan_management", current_lang), key="menu_plan", 
                        type="primary" if st.session_state.current_page == 'plan_management' else "secondary", use_container_width=True):
                set_page('plan_management')
                st.rerun()
        
        # 관리자인 경우 추가 메뉴
        if st.session_state.role == 'admin':
            admin_cols = st.columns([5, 1])
            with admin_cols[1]:
                if st.button(get_text("admin_settings", current_lang), key="menu_admin", 
                            type="primary" if st.session_state.current_page == 'admin_settings' else "secondary", use_container_width=True):
                    set_page('admin_settings')
                    st.rerun()
        
        # 컨텐츠 표시
        if st.session_state.current_page == 'dashboard':
            dashboard_component.render()
        elif st.session_state.current_page == 'equipment_detail':
            equipment_detail_component.render()
        elif st.session_state.current_page == 'data_input':
            data_input_component.render()
        elif st.session_state.current_page == 'reports':
            reports_component.render()
        elif st.session_state.current_page == 'plan_management':
            plan_management_component.render()
        elif st.session_state.current_page == 'plan_suspension':
            plan_suspension_component.render()
        elif st.session_state.current_page == 'equipment_status_detail':
            equipment_status_detail_component.render()
        elif st.session_state.current_page == 'admin_settings':
            admin_component.render()