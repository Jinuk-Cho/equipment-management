"""
데이터 처리 관련 공통 기능을 위한 모듈
- 일반 데이터 조회/저장 기능
- 설비 관련 데이터 처리
- 오류 코드 관련 데이터 처리
- 사용자 관련 데이터 처리
- 계획 관련 데이터 처리
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from supabase.client import create_client, Client
from utils.supabase_client import get_supabase_client
from components.language import get_text
import plotly.express as px
import numpy as np
import re
import io
import base64

def get_all_equipment_data(lang='ko'):
    """
    모든 설비 데이터를 조회합니다.
    
    Args:
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        pd.DataFrame: 설비 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 모든 설비 데이터 조회
        response = supabase.table('equipment').select('*').execute()
        
        if response.data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def get_equipment_by_number(equipment_number, lang='ko'):
    """
    설비 번호로 설비 데이터를 조회합니다.
    
    Args:
        equipment_number (str): 설비 번호
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        dict: 설비 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 설비 번호로 설비 데이터 조회
        response = supabase.table('equipment').select('*').eq('equipment_number', equipment_number).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_all_error_codes(lang='ko'):
    """
    모든 오류 코드 데이터를 조회합니다.
    
    Args:
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        pd.DataFrame: 오류 코드 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 모든 오류 코드 데이터 조회
        response = supabase.table('error_codes').select('*').execute()
        
        if response.data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def get_error_by_code(error_code, lang='ko'):
    """
    오류 코드로 오류 데이터를 조회합니다.
    
    Args:
        error_code (str): 오류 코드
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        dict: 오류 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 오류 코드로 오류 데이터 조회
        response = supabase.table('error_codes').select('*').eq('code', error_code).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_all_users(lang='ko'):
    """
    모든 사용자 데이터를 조회합니다.
    
    Args:
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        pd.DataFrame: 사용자 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 모든 사용자 데이터 조회
        response = supabase.table('users').select('*').execute()
        
        if response.data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def get_user_by_username(username, lang='ko'):
    """
    사용자 이름으로 사용자 데이터를 조회합니다.
    
    Args:
        username (str): 사용자 이름
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        dict: 사용자 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 사용자 이름으로 사용자 데이터 조회
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def save_error_record(error_data, lang='ko'):
    """
    오류 기록을 저장합니다.
    
    Args:
        error_data (dict): 오류 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 오류 기록 저장
        response = supabase.table('error_records').insert(error_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def save_parts_replacement(parts_data, lang='ko'):
    """
    부품 교체 기록을 저장합니다.
    
    Args:
        parts_data (dict): 부품 교체 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 부품 교체 기록 저장
        response = supabase.table('parts_replacements').insert(parts_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def save_model_change(model_data, lang='ko'):
    """
    모델 변경 기록을 저장합니다.
    
    Args:
        model_data (dict): 모델 변경 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 모델 변경 기록 저장
        response = supabase.table('model_changes').insert(model_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def save_equipment_stop(stop_data, lang='ko'):
    """
    설비 정지 기록을 저장합니다.
    
    Args:
        stop_data (dict): 설비 정지 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 설비 정지 기록 저장
        response = supabase.table('equipment_stops').insert(stop_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def get_maintenance_plans(equipment_number=None, lang='ko'):
    """
    유지보수 계획을 조회합니다.
    
    Args:
        equipment_number (str): 설비 번호 (None인 경우 모든 계획)
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        pd.DataFrame: 유지보수 계획 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 쿼리 생성
        query = supabase.table('maintenance_plans').select('*')
        
        # 설비 번호가 지정된 경우 필터링
        if equipment_number:
            query = query.eq('equipment_number', equipment_number)
        
        # 쿼리 실행
        response = query.execute()
        
        if response.data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def save_maintenance_plan(plan_data, lang='ko'):
    """
    유지보수 계획을 저장합니다.
    
    Args:
        plan_data (dict): 유지보수 계획 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 유지보수 계획 저장
        response = supabase.table('maintenance_plans').insert(plan_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def save_plan_suspension(suspension_data, lang='ko'):
    """
    계획 중단 기록을 저장합니다.
    
    Args:
        suspension_data (dict): 계획 중단 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 저장 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 계획 중단 기록 저장
        response = supabase.table('plan_suspensions').insert(suspension_data).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def get_plan_suspensions(plan_id=None, active_only=False, lang='ko'):
    """
    계획 중단 기록을 조회합니다.
    
    Args:
        plan_id (str): 계획 ID (None인 경우 모든 중단 기록)
        active_only (bool): 활성화된 중단 기록만 조회할지 여부
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        pd.DataFrame: 계획 중단 기록 데이터
    """
    supabase = get_supabase_client()
    
    try:
        # 쿼리 생성
        query = supabase.table('plan_suspensions').select('*')
        
        # 계획 ID가 지정된 경우 필터링
        if plan_id:
            query = query.eq('plan_id', plan_id)
        
        # 활성화된 중단 기록만 조회하는 경우 필터링
        if active_only:
            today = date.today().isoformat()
            query = query.is_('end_date', 'null').or_(f"end_date.gte.{today}")
        
        # 쿼리 실행
        response = query.execute()
        
        if response.data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def update_plan_suspension(suspension_id, update_data, lang='ko'):
    """
    계획 중단 기록을 업데이트합니다.
    
    Args:
        suspension_id (str): 중단 기록 ID
        update_data (dict): 업데이트할 데이터
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        bool: 업데이트 성공 여부
    """
    supabase = get_supabase_client()
    
    try:
        # 계획 중단 기록 업데이트
        response = supabase.table('plan_suspensions').update(update_data).eq('id', suspension_id).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def convert_image_to_base64(image_bytes):
    """
    이미지 바이트를 Base64 문자열로 변환합니다.
    
    Args:
        image_bytes (bytes): 이미지 바이트
        
    Returns:
        str: Base64 인코딩된 이미지 문자열
    """
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image

def parse_date_string(date_str):
    """
    날짜 문자열을 datetime.date 객체로 파싱합니다.
    
    Args:
        date_str (str): 날짜 문자열 (YYYY-MM-DD 형식)
        
    Returns:
        date: 파싱된 날짜 객체
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        try:
            return datetime.strptime(date_str, "%Y/%m/%d").date()
        except:
            return None 