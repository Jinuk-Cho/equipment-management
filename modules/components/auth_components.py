"""
인증 관련 공통 컴포넌트를 위한 모듈
- 로그인 폼
- 사용자 프로필 관리
- 권한 확인
- 세션 관리
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from components.language import get_text
from utils.supabase_client import get_supabase_client
import time
import re

def render_login_form(lang='ko'):
    """
    로그인 폼을 렌더링합니다.
    
    Args:
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 로그인 성공 여부
    """
    st.title(get_text("login", lang))
    
    # 로그인 폼
    with st.form("login_form"):
        # 사용자 이름 입력
        username = st.text_input(get_text("username", lang))
        
        # 비밀번호 입력
        password = st.text_input(get_text("password", lang), type="password")
        
        # 로그인 버튼
        submit_button = st.form_submit_button(get_text("login", lang))
        
        if submit_button:
            # 로그인 검증
            if check_credentials(username, password):
                # 로그인 성공
                st.success(get_text("login_success", lang))
                
                # 사용자 정보 조회
                user_info = get_user_info(username)
                
                # 세션 상태 설정
                st.session_state.user = username
                st.session_state.role = user_info.get('role', 'user')
                st.session_state.last_activity = time.time()
                
                return True
            else:
                # 로그인 실패
                st.error(get_text("login_failed", lang))
                return False
    
    return False

def check_credentials(username, password):
    """
    사용자 인증 정보를 확인합니다.
    
    Args:
        username (str): 사용자 이름
        password (str): 비밀번호
        
    Returns:
        bool: 인증 성공 여부
    """
    if not username or not password:
        return False
    
    supabase = get_supabase_client()
    
    try:
        # 사용자 조회
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if not response.data:
            return False
        
        user_data = response.data[0]
        
        # 비밀번호 확인 (실제 환경에서는 암호화된 비밀번호 비교 필요)
        if user_data.get('password') == password:
            return True
        
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def get_user_info(username):
    """
    사용자 정보를 조회합니다.
    
    Args:
        username (str): 사용자 이름
        
    Returns:
        dict: 사용자 정보
    """
    supabase = get_supabase_client()
    
    try:
        # 사용자 조회
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            return {}
    except Exception as e:
        st.error(f"Error: {e}")
        return {}

def is_user_logged_in():
    """
    사용자가 로그인되어 있는지 확인합니다.
    
    Returns:
        bool: 로그인 여부
    """
    return 'user' in st.session_state and st.session_state.user

def is_admin():
    """
    현재 로그인한 사용자가 관리자인지 확인합니다.
    
    Returns:
        bool: 관리자 여부
    """
    return is_user_logged_in() and 'role' in st.session_state and st.session_state.role == 'admin'

def check_session_expired(timeout_minutes=30, lang='ko'):
    """
    세션 만료 여부를 확인합니다.
    
    Args:
        timeout_minutes (int): 세션 타임아웃 시간(분)
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 세션 만료 여부
    """
    if not is_user_logged_in():
        return False
    
    # 마지막 활동 시간 확인
    if 'last_activity' not in st.session_state:
        logout_user()
        return True
    
    # 마지막 활동 시간과 현재 시간의 차이 계산
    elapsed_time = time.time() - st.session_state.last_activity
    
    # 타임아웃 시간(초) 계산
    timeout_seconds = timeout_minutes * 60
    
    # 세션 만료 확인
    if elapsed_time > timeout_seconds:
        # 세션 만료 메시지 표시
        st.warning(get_text("session_expired", lang))
        
        # 로그아웃 처리
        logout_user()
        
        return True
    
    # 활동 시간 갱신
    st.session_state.last_activity = time.time()
    
    return False

def logout_user():
    """
    사용자를 로그아웃 처리합니다.
    """
    # 세션 상태에서 사용자 정보 제거
    if 'user' in st.session_state:
        del st.session_state.user
    
    if 'role' in st.session_state:
        del st.session_state.role
    
    if 'last_activity' in st.session_state:
        del st.session_state.last_activity

def render_user_profile(lang='ko'):
    """
    사용자 프로필 페이지를 렌더링합니다.
    
    Args:
        lang (str): 언어 코드 ('ko' 또는 'vi')
    """
    if not is_user_logged_in():
        st.error(get_text("login_required", lang))
        return
    
    st.title(get_text("user_profile", lang))
    
    # 사용자 정보 조회
    user_info = get_user_info(st.session_state.user)
    
    if not user_info:
        st.error(get_text("user_not_found", lang))
        return
    
    # 사용자 정보 표시
    st.subheader(get_text("profile_info", lang))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{get_text('username', lang)}:** {user_info.get('username', '')}")
        st.write(f"**{get_text('name', lang)}:** {user_info.get('name', '')}")
    
    with col2:
        st.write(f"**{get_text('role', lang)}:** {user_info.get('role', '')}")
        st.write(f"**{get_text('email', lang)}:** {user_info.get('email', '')}")
    
    # 프로필 수정 폼
    st.subheader(get_text("edit_profile", lang))
    
    with st.form("profile_form"):
        # 이름 입력
        name = st.text_input(get_text("name", lang), value=user_info.get('name', ''))
        
        # 이메일 입력
        email = st.text_input(get_text("email", lang), value=user_info.get('email', ''))
        
        # 현재 비밀번호 입력
        current_password = st.text_input(get_text("current_password", lang), type="password")
        
        # 새 비밀번호 입력
        new_password = st.text_input(get_text("new_password", lang), type="password")
        
        # 새 비밀번호 확인
        confirm_password = st.text_input(get_text("confirm_password", lang), type="password")
        
        # 저장 버튼
        submit_button = st.form_submit_button(get_text("save", lang))
        
        if submit_button:
            # 현재 비밀번호 확인
            if current_password and not check_credentials(user_info.get('username', ''), current_password):
                st.error(get_text("wrong_password", lang))
                return
            
            # 새 비밀번호 확인
            if new_password and new_password != confirm_password:
                st.error(get_text("password_mismatch", lang))
                return
            
            # 업데이트할 데이터 생성
            update_data = {}
            
            if name:
                update_data['name'] = name
            
            if email:
                # 이메일 형식 검증
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error(get_text("invalid_email", lang))
                    return
                
                update_data['email'] = email
            
            if new_password:
                # 비밀번호 유효성 검사 (최소 8자, 영문자, 숫자, 특수문자 포함)
                if len(new_password) < 8:
                    st.error(get_text("password_too_short", lang))
                    return
                
                update_data['password'] = new_password
            
            if update_data:
                # 프로필 업데이트
                if update_user_profile(user_info.get('id'), update_data):
                    st.success(get_text("profile_updated", lang))
                else:
                    st.error(get_text("profile_update_failed", lang))

def update_user_profile(user_id, update_data):
    """
    사용자 프로필을 업데이트합니다.
    
    Args:
        user_id (str): 사용자 ID
        update_data (dict): 업데이트할 데이터
        
    Returns:
        bool: 업데이트 성공 여부
    """
    if not user_id or not update_data:
        return False
    
    supabase = get_supabase_client()
    
    try:
        # 사용자 프로필 업데이트
        response = supabase.table('users').update(update_data).eq('id', user_id).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False 