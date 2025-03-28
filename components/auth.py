def show_login():
    """로그인 화면을 표시합니다."""
    st.markdown('<div style="text-align: center; margin: 2rem 0;"><h1>ALMUS CNC 설비 관리 시스템</h1></div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")
        
        if submitted:
            if authenticate_user(username, password):
                st.session_state["is_authenticated"] = True
                st.session_state["username"] = username
                st.experimental_rerun()
            else:
                st.error("잘못된 사용자 이름 또는 비밀번호입니다.")

def handle_logout():
    """로그아웃 처리를 수행합니다."""
    if st.session_state.get("is_authenticated"):
        st.session_state["is_authenticated"] = False
        st.session_state["username"] = None
        st.experimental_rerun()

def check_authentication():
    """사용자 인증 상태를 확인합니다."""
    if not st.session_state.get("is_authenticated"):
        show_login()
        st.stop()
    
    # URL 파라미터 확인
    params = st.experimental_get_query_params()
    if params.get("action") == ["logout"]:
        handle_logout()
    elif params.get("page") == ["profile"]:
        show_profile()

def show_profile():
    """사용자 프로필 페이지를 표시합니다."""
    st.title("사용자 프로필")
    
    username = st.session_state.get("username", "")
    st.write(f"### 사용자 정보")
    st.write(f"- 사용자 이름: {username}")
    st.write(f"- 권한: {'관리자' if username == 'admin' else '일반 사용자'}")
    
    # 프로필 수정 기능 (필요한 경우 추가)
    with st.expander("프로필 수정"):
        st.write("프로필 수정 기능은 현재 개발 중입니다.") 