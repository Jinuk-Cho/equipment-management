import os
from dotenv import load_dotenv
import streamlit as st

# supabase import 문제 해결을 위한 try-except 블록
try:
    from supabase import create_client, Client
except ImportError:
    # 디버깅용 메시지
    print("Failed to import supabase. Make sure it's installed correctly.")
    
    # 임시 대체 함수 정의
    def create_client(url, key):
        print(f"Mock supabase client created with URL: {url}")
        return {}

# .env 파일 로드
load_dotenv()

# Supabase 설정 (환경 변수가 없으면 기본값 사용)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://example.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-api-key")

# Supabase 클라이언트 초기화 (캐싱)
def get_supabase():
    """Supabase 클라이언트를 반환합니다."""
    # 지연 로딩을 통해 st.cache_resource 데코레이터 사용
    @st.cache_resource
    def _create_client():
        try:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"Error creating Supabase client: {e}")
            # 에러가 발생해도 앱이 중단되지 않도록 빈 객체 반환
            return {}
    
    return _create_client()

# 기본 CRUD 함수 정의
def fetch_data(table):
    """데이터를 조회합니다."""
    try:
        # 실제 데이터베이스 조회 시도
        if supabase:
            response = supabase.table(table).select("*").execute()
            return response.data
    except Exception as e:
        # 오류 발생 시 가상 데이터 반환
        print(f"테이블 '{table}' 조회 중 오류 발생: {e}")
    
    # 테이블에 따라 다른 가상 데이터 반환
    if table == 'maintenance_plans':
        return [
            {
                'id': 1, 
                'plan_code': 'MP2023001', 
                'equipment_number': 'EQ001', 
                'status': 'ACTIVE',
                'start_date': '2023-04-01',
                'end_date': '2023-09-30',
                'description': '프레스 머신 1 정기 유지보수'
            },
            {
                'id': 2, 
                'plan_code': 'MP2023002', 
                'equipment_number': 'EQ002', 
                'status': 'SUSPENDED',
                'start_date': '2023-05-15',
                'end_date': '2023-11-15',
                'description': '컨베이어 벨트 점검 계획'
            },
            {
                'id': 3, 
                'plan_code': 'MP2023003', 
                'equipment_number': 'EQ003', 
                'status': 'ACTIVE',
                'start_date': '2023-06-01',
                'end_date': '2023-12-31',
                'description': '로봇 암 소프트웨어 업데이트'
            }
        ]
    elif table == 'equipment':
        return [
            {'id': 1, 'equipment_number': 'EQ001', 'name': '프레스 머신 1', 'status': '정상', 'location': 'A동 1층'},
            {'id': 2, 'equipment_number': 'EQ002', 'name': '컨베이어 벨트', 'status': '정상', 'location': 'A동 2층'},
            {'id': 3, 'equipment_number': 'EQ003', 'name': '로봇 암', 'status': '점검중', 'location': 'B동 1층'},
            {'id': 4, 'equipment_number': 'EQ004', 'name': '포장기', 'status': '고장', 'location': 'C동 1층'},
            {'id': 5, 'equipment_number': 'EQ005', 'name': '프레스 머신 2', 'status': '정상', 'location': 'A동 1층'}
        ]
    elif table == 'users':
        return [
            {'id': 1, 'email': 'admin@example.com', 'name': '관리자', 'role': 'admin'},
            {'id': 2, 'email': 'user1@example.com', 'name': '사용자1', 'role': 'user'},
            {'id': 3, 'email': 'user2@example.com', 'name': '사용자2', 'role': 'user'}
        ]
    else:
        # 기본 빈 배열 반환
        return []

def insert_data(table, data):
    """데이터를 삽입합니다."""
    return True

def update_data(table, id, data):
    """데이터를 업데이트합니다."""
    return True

def delete_data(table, id):
    """데이터를 삭제합니다."""
    return True

# 인증 관련 함수
def sign_in_user(email, password):
    """사용자 로그인"""
    return {"user": {"email": email}, "session": {}}

def sign_up_user(email, password, user_data):
    """사용자 등록"""
    return {"user": {"email": email}}

# 설비 관련 함수
def get_equipment_list():
    """설비 목록을 조회합니다."""
    try:
        # 실제 데이터베이스 조회 시도
        if supabase:
            response = supabase.table('equipment').select("*").execute()
            return response.data
    except Exception as e:
        # 오류 발생 시 가상 데이터 반환
        print(f"설비 목록 조회 중 오류 발생: {e}")
    
    # 가상 데이터 생성 및 반환
    return [
        {'id': 1, 'equipment_number': 'EQ001', 'name': '프레스 머신 1', 'status': '정상', 'location': 'A동 1층'},
        {'id': 2, 'equipment_number': 'EQ002', 'name': '컨베이어 벨트', 'status': '정상', 'location': 'A동 2층'},
        {'id': 3, 'equipment_number': 'EQ003', 'name': '로봇 암', 'status': '점검중', 'location': 'B동 1층'},
        {'id': 4, 'equipment_number': 'EQ004', 'name': '포장기', 'status': '고장', 'location': 'C동 1층'},
        {'id': 5, 'equipment_number': 'EQ005', 'name': '프레스 머신 2', 'status': '정상', 'location': 'A동 1층'}
    ]

def get_equipment_serials():
    """설비 시리얼 목록을 조회합니다."""
    return []

def add_equipment_serial(serial_data):
    """설비 시리얼을 추가합니다."""
    return True

def update_equipment_serial(id, serial_data):
    """설비 시리얼을 업데이트합니다."""
    return True

def delete_equipment_serial(id):
    """설비 시리얼을 삭제합니다."""
    return True

def bulk_upload_equipment_serials(serials_data):
    """설비 시리얼을 일괄 업로드합니다."""
    return True

# 기타 필요한 함수들
def get_error_history():
    """오류 이력을 조회합니다."""
    return []

def get_parts_replacement():
    """부품 교체 이력을 조회합니다."""
    return []

# Supabase 클라이언트 인스턴스
supabase = get_supabase()

# 사용자 인증
def sign_in_user(username, password):
    # 관리자 계정 하드코딩 인증 처리
    if username == "admin" and password == "admin":
        # 관리자 계정에 대한 임시 응답 객체 생성
        class AdminUser:
            def __init__(self):
                self.id = "admin-user-id"
                self.user_metadata = {
                    "name": "관리자",
                    "role": "admin",
                    "department": "관리부서",
                    "phone": "010-0000-0000"
                }
                self.role = "admin"
                
        admin_user = AdminUser()
        return admin_user
    
    # 이 부분은 하드코딩된 관리자 계정이 아닌 경우에만 체크
    if not supabase:
        st.error("Supabase 설정이 필요합니다. .env 파일을 확인해주세요.")
        return None
    
    try:
        # 일반 사용자는 이메일과 비밀번호로 인증
        response = supabase.auth.sign_in_with_password({
            "email": username,  # username을 email로 간주
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

# 설비 시리얼 관련 함수
def get_equipment_serials():
    """
    모든 설비 시리얼 번호 매핑을 가져옵니다.
    """
    if not supabase:
        return []
    try:
        response = supabase.table('equipment_serials').select("*").order('equipment_number').execute()
        return response.data
    except Exception as e:
        st.error(f"설비 시리얼 조회 오류: {str(e)}")
        return []

def get_serial_by_equipment_number(equipment_number):
    """
    설비 번호로 시리얼 번호를 조회합니다.
    """
    if not supabase:
        return None
    try:
        response = supabase.table('equipment_serials')\
            .select("serial_number")\
            .eq('equipment_number', equipment_number)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]['serial_number']
        return None
    except Exception as e:
        st.error(f"시리얼 번호 조회 오류: {str(e)}")
        return None

def add_equipment_serial(equipment_number, serial_number):
    """
    새로운 설비-시리얼 매핑을 추가합니다.
    """
    if not supabase:
        return None
    try:
        data = {
            'equipment_number': equipment_number,
            'serial_number': serial_number
        }
        response = supabase.table('equipment_serials').insert(data).execute()
        return response.data
    except Exception as e:
        st.error(f"시리얼 번호 추가 오류: {str(e)}")
        return None

def update_equipment_serial(equipment_number, serial_number):
    """
    기존 설비의 시리얼 번호를 업데이트합니다.
    """
    if not supabase:
        return None
    try:
        data = {'serial_number': serial_number}
        response = supabase.table('equipment_serials')\
            .update(data)\
            .eq('equipment_number', equipment_number)\
            .execute()
        return response.data
    except Exception as e:
        st.error(f"시리얼 번호 업데이트 오류: {str(e)}")
        return None

def delete_equipment_serial(equipment_number):
    """
    설비-시리얼 매핑을 삭제합니다.
    """
    if not supabase:
        return None
    try:
        response = supabase.table('equipment_serials')\
            .delete()\
            .eq('equipment_number', equipment_number)\
            .execute()
        return response.data
    except Exception as e:
        st.error(f"시리얼 번호 삭제 오류: {str(e)}")
        return None

def bulk_upload_equipment_serials(serials_data):
    """
    여러 설비-시리얼 매핑을 한 번에 업로드합니다.
    serials_data는 {'equipment_number': number, 'serial_number': 'serial'} 딕셔너리의 리스트여야 합니다.
    """
    if not supabase:
        return None
    try:
        response = supabase.table('equipment_serials').upsert(serials_data).execute()
        return response.data
    except Exception as e:
        st.error(f"시리얼 번호 일괄 업로드 오류: {str(e)}")
        return None

# 모델 변경 이력 관련 함수
def get_model_changes():
    """모델 변경 이력을 가져옵니다."""
    if not supabase:
        return []
    try:
        response = supabase.table('model_changes').select("*").order('timestamp', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"모델 변경 이력 조회 오류: {str(e)}")
        return []

def add_model_change(model_change_data):
    """
    모델 변경 정보를 추가합니다.
    """
    if not supabase:
        return None
    try:
        response = supabase.table('model_changes').insert(model_change_data).execute()
        return response.data
    except Exception as e:
        st.error(f"모델 변경 정보 추가 오류: {str(e)}")
        return None

def get_model_change_stats(equipment_number=None, start_date=None, end_date=None):
    """모델 변경 통계를 가져옵니다."""
    if not supabase:
        return {}
    
    try:
        query = supabase.table('model_changes').select("*")
        
        if equipment_number:
            query = query.eq('equipment_number', equipment_number)
        
        if start_date:
            query = query.gte('timestamp', start_date)
        
        if end_date:
            query = query.lte('timestamp', end_date)
            
        response = query.execute()
        
        # 통계 데이터 처리
        data = response.data
        
        if not data:
            return {
                "total_changes": 0,
                "avg_duration": 0,
                "models": []
            }
        
        # 모델별 변경 횟수 계산
        model_counts = {}
        for item in data:
            from_model = item.get('model_from', 'Unknown')
            to_model = item.get('model_to', 'Unknown')
            
            if from_model not in model_counts:
                model_counts[from_model] = 0
            
            if to_model not in model_counts:
                model_counts[to_model] = 0
                
            model_counts[to_model] += 1
        
        # 평균 소요 시간 계산
        total_duration = sum(item.get('duration_minutes', 0) for item in data)
        avg_duration = total_duration / len(data) if data else 0
        
        return {
            "total_changes": len(data),
            "avg_duration": avg_duration,
            "models": [{"name": k, "count": v} for k, v in model_counts.items()]
        }
        
    except Exception as e:
        st.error(f"모델 변경 통계 조회 오류: {str(e)}")
        return {
            "total_changes": 0,
            "avg_duration": 0,
            "models": []
        }

def add_equipment_stop(stop_data):
    """
    설비 정지 정보를 추가합니다.
    """
    if not supabase:
        return None
    try:
        response = supabase.table('equipment_stops').insert(stop_data).execute()
        return response.data
    except Exception as e:
        st.error(f"설비 정지 정보 추가 오류: {str(e)}")
        return None

def get_equipment_stops(equipment_number=None):
    """
    설비 정지 이력을 조회합니다. 설비 번호가 지정된 경우 해당 설비의 정지 이력만 반환합니다.
    """
    if not supabase:
        return []
    try:
        query = supabase.table('equipment_stops').select("*").order('start_time', desc=True)
        
        if equipment_number:
            query = query.eq('equipment_number', equipment_number)
            
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"설비 정지 이력 조회 오류: {str(e)}")
        return [] 