import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

# .env 파일 로드
load_dotenv()

# Supabase 클라이언트 초기화
def init_connection():
    try:
        # 1. Streamlit Secrets에서 시도
        try:
            supabase_url = st.secrets["SUPABASE_URL"]
            supabase_key = st.secrets["SUPABASE_KEY"]
        except Exception:
            # 2. 환경 변수에서 시도
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            # 3. 직접 하드코딩된 값 사용 (최후의 수단)
            if not supabase_url or not supabase_key:
                supabase_url = "https://wgecephqtnpeicfqnwrg.supabase.co"
                supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnZWNlcGhxdG5wZWljZnFud3JnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1NDE0NzksImV4cCI6MjA1ODExNzQ3OX0.dfgp94tqlhb0fAh0ory5EUAwmP7TpQowlwf5s7Kg8uo"
        
        if not supabase_url or not supabase_key:
            st.error("Supabase 설정이 필요합니다.")
            return None
            
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"Supabase 연결 오류: {str(e)}")
        return None

# Supabase 클라이언트 초기화 (캐싱)
@st.cache_resource
def get_supabase():
    return init_connection()

# Supabase 클라이언트 인스턴스
supabase = get_supabase()

# 사용자 인증
def sign_in_user(email, password):
    # 관리자 계정 하드코딩 인증 처리
    if email == "admin" and password == "admin":
        # 관리자 계정에 대한 임시 응답 객체 생성
        class AdminUser:
            def __init__(self):
                self.id = "admin-user-id"
                self.email = "admin@example.com"
                self.role = "admin"
                
        admin_user = AdminUser()
        return admin_user
    
    # 이 부분은 하드코딩된 관리자 계정이 아닌 경우에만 체크
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
    if not supabase:
        return []
    try:
        response = supabase.table('equipment').select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def add_equipment(equipment_data):
    if not supabase:
        return None
    try:
        response = supabase.table('equipment').insert(equipment_data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 오류: {str(e)}")
        return None

def update_equipment(equipment_id, equipment_data):
    if not supabase:
        return None
    try:
        response = supabase.table('equipment').update(equipment_data).eq('id', equipment_id).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 수정 오류: {str(e)}")
        return None

# 에러 이력 관련 함수
def get_error_history():
    if not supabase:
        return []
    try:
        response = supabase.table('error_history').select("*").order('timestamp', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def add_error_history(error_data):
    if not supabase:
        return None
    try:
        response = supabase.table('error_history').insert(error_data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 오류: {str(e)}")
        return None

# 부품 교체 관련 함수
def get_parts_replacement():
    if not supabase:
        return []
    try:
        response = supabase.table('parts_replacement').select("*").order('timestamp', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def add_parts_replacement(parts_data):
    if not supabase:
        return None
    try:
        response = supabase.table('parts_replacement').insert(parts_data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 오류: {str(e)}")
        return None

# 에러 코드 관련 함수
def get_error_codes():
    if not supabase:
        return []
    try:
        response = supabase.table('error_codes').select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def add_error_code(error_code_data):
    if not supabase:
        return None
    try:
        response = supabase.table('error_codes').insert(error_code_data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 오류: {str(e)}")
        return None

# 부품 목록 관련 함수
def get_parts_list():
    if not supabase:
        return []
    try:
        response = supabase.table('parts').select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def add_part(part_data):
    if not supabase:
        return None
    try:
        response = supabase.table('parts').insert(part_data).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 추가 오류: {str(e)}")
        return None

def update_part_stock(part_id, new_stock):
    if not supabase:
        return None
    try:
        response = supabase.table('parts_list').update({'stock': new_stock}).eq('id', part_id).execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 수정 오류: {str(e)}")
        return None

# 통계 관련 함수
def get_error_stats(start_date=None, end_date=None):
    if not supabase:
        return []
    try:
        query = supabase.table('error_history').select("*")
        if start_date:
            query = query.gte('timestamp', start_date)
        if end_date:
            query = query.lte('timestamp', end_date)
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return []

def get_parts_stats(start_date=None, end_date=None):
    if not supabase:
        return []
    try:
        query = supabase.table('parts_replacement').select("*")
        if start_date:
            query = query.gte('timestamp', start_date)
        if end_date:
            query = query.lte('timestamp', end_date)
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"데이터 조회 오류: {str(e)}")
        return [] 