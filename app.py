import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from utils.auth import check_password, login_user
from utils.google_sheet import get_sheet_data
from components.dashboard import show_dashboard
from components.equipment_detail import show_equipment_detail
from components.data_input import show_data_input
from components.reports import show_reports
from components.admin import show_admin_settings

# 페이지 설정
st.set_page_config(
    page_title="설비 관리 시스템",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

# 로그인하지 않은 경우 로그인 페이지 표시
if not st.session_state['logged_in']:
    st.title("설비 관리 시스템 로그인")
    
    login_type = st.radio("로그인 방식 선택", ["일반 로그인", "Google 계정 로그인"])
    
    if login_type == "일반 로그인":
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        
        if st.button("로그인"):
            if check_password(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("잘못된 아이디 또는 비밀번호입니다.")
    else:
        if st.button("Google 계정으로 로그인"):
            # Google OAuth2 로그인 처리
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/client_secrets.json',
                ['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            credentials = flow.run_local_server(port=8501)
            st.session_state['credentials'] = credentials
            st.session_state['logged_in'] = True
            st.rerun()

else:
    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["실시간 대시보드", "장비 상세 조회", "데이터 입력", "보고서 및 통계", "관리자 설정"]
    )
    
    # 선택된 메뉴에 따라 해당 컴포넌트 표시
    if menu == "실시간 대시보드":
        show_dashboard()
    elif menu == "장비 상세 조회":
        show_equipment_detail()
    elif menu == "데이터 입력":
        show_data_input()
    elif menu == "보고서 및 통계":
        show_reports()
    elif menu == "관리자 설정" and st.session_state['user_role'] == 'admin':
        show_admin_settings()
    elif menu == "관리자 설정":
        st.error("관리자 권한이 필요합니다.")
    
    # 로그아웃 버튼
    if st.sidebar.button("로그아웃"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.rerun()