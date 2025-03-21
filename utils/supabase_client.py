from supabase import create_client
import streamlit as st
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Supabase 클라이언트 초기화
def init_supabase():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        st.error("Supabase 설정이 필요합니다. .env 파일을 확인해주세요.")
        return None
    
    return create_client(supabase_url, supabase_key)

# 사용자 인증
def sign_in_user(email, password):
    client = init_supabase()
    if not client:
        return None
    
    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password,
            "options": {
                "emailRedirectTo": "http://localhost:8506"
            }
        })
        return response.user
    except Exception as e:
        st.error(f"로그인 실패: {str(e)}")
        return None

# 사용자 등록
def sign_up_user(email, password, role="user"):
    client = init_supabase()
    if not client:
        return None
    
    try:
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "role": role
                },
                "emailRedirectTo": "http://localhost:8506"
            }
        })
        return response.user
    except Exception as e:
        st.error(f"회원가입 실패: {str(e)}")
        return None

# 데이터 조회
def fetch_data(table_name):
    client = init_supabase()
    if not client:
        return None
    
    try:
        response = client.table(table_name).select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 실패: {str(e)}")
        return None

# 데이터 추가
def insert_data(table_name, data):
    client = init_supabase()
    if not client:
        return False
    
    try:
        client.table(table_name).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"데이터 추가 실패: {str(e)}")
        return False

# 데이터 수정
def update_data(table_name, data, match_column, match_value):
    client = init_supabase()
    if not client:
        return False
    
    try:
        client.table(table_name)\
            .update(data)\
            .eq(match_column, match_value)\
            .execute()
        return True
    except Exception as e:
        st.error(f"데이터 수정 실패: {str(e)}")
        return False

# 데이터 삭제
def delete_data(table_name, match_column, match_value):
    client = init_supabase()
    if not client:
        return False
    
    try:
        client.table(table_name)\
            .delete()\
            .eq(match_column, match_value)\
            .execute()
        return True
    except Exception as e:
        st.error(f"데이터 삭제 실패: {str(e)}")
        return False 