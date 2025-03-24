import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

# .env 파일 로드
load_dotenv()

# Supabase 클라이언트 초기화
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# 사용자 인증
def sign_in_user(email, password):
    if not supabase:
        st.error("Supabase 설정이 필요합니다. .env 파일을 확인해주세요.")
        return None
    
    try:
        response = supabase.auth.sign_in_with_password({
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
    if not supabase:
        return None
    
    try:
        response = supabase.auth.sign_up({
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
    if not supabase:
        return None
    
    try:
        response = supabase.table(table_name).select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 실패: {str(e)}")
        return None

# 데이터 추가
def insert_data(table_name, data):
    if not supabase:
        return False
    
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 실패: {str(e)}")
        return False

# 데이터 수정
def update_data(table_name, data, match_column, match_value):
    if not supabase:
        return False
    
    try:
        response = supabase.table(table_name)\
            .update(data)\
            .eq(match_column, match_value)\
            .execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 수정 실패: {str(e)}")
        return False

# 데이터 삭제
def delete_data(table_name, match_column, match_value):
    if not supabase:
        return False
    
    try:
        response = supabase.table(table_name)\
            .delete()\
            .eq(match_column, match_value)\
            .execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 삭제 실패: {str(e)}")
        return False

# 설비 목록 관련 함수
def get_equipment_list():
    response = supabase.table('equipment_list').select("*").execute()
    return response.data

def add_equipment(equipment_data):
    response = supabase.table('equipment_list').insert(equipment_data).execute()
    return response.data

def update_equipment(equipment_id, equipment_data):
    response = supabase.table('equipment_list').update(equipment_data).eq('id', equipment_id).execute()
    return response.data

# 에러 이력 관련 함수
def get_error_history():
    response = supabase.table('error_history').select("*").order('timestamp', desc=True).execute()
    return response.data

def add_error_history(error_data):
    response = supabase.table('error_history').insert(error_data).execute()
    return response.data

# 부품 교체 관련 함수
def get_parts_replacement():
    response = supabase.table('parts_replacement').select("*").order('timestamp', desc=True).execute()
    return response.data

def add_parts_replacement(parts_data):
    response = supabase.table('parts_replacement').insert(parts_data).execute()
    return response.data

# 에러 코드 관련 함수
def get_error_codes():
    response = supabase.table('error_codes').select("*").execute()
    return response.data

def add_error_code(error_code_data):
    response = supabase.table('error_codes').insert(error_code_data).execute()
    return response.data

# 부품 목록 관련 함수
def get_parts_list():
    response = supabase.table('parts_list').select("*").execute()
    return response.data

def add_part(part_data):
    response = supabase.table('parts_list').insert(part_data).execute()
    return response.data

def update_part_stock(part_id, new_stock):
    response = supabase.table('parts_list').update({'stock': new_stock}).eq('id', part_id).execute()
    return response.data

# 통계 관련 함수
def get_error_stats(start_date=None, end_date=None):
    query = supabase.table('error_history').select("*")
    if start_date:
        query = query.gte('timestamp', start_date)
    if end_date:
        query = query.lte('timestamp', end_date)
    response = query.execute()
    return response.data

def get_parts_stats(start_date=None, end_date=None):
    query = supabase.table('parts_replacement').select("*")
    if start_date:
        query = query.gte('timestamp', start_date)
    if end_date:
        query = query.lte('timestamp', end_date)
    response = query.execute()
    return response.data 