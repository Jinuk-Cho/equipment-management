"""
양식 관련 공통 컴포넌트를 위한 모듈
- 텍스트 입력 필드
- 숫자 입력 필드
- 선택 입력 필드
- 날짜 선택 필드
- 시간 선택 필드
- 파일 업로드 필드
- 에러 메시지 표시
"""

import streamlit as st
from components.language import get_text
import pandas as pd
from datetime import datetime, date

def render_text_input(label, key, placeholder="", lang="ko", required=False, disabled=False, value="", help_text=""):
    """
    텍스트 입력 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        key (str): 입력 필드의 고유 키
        placeholder (str): 플레이스홀더 텍스트
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        value (str): 기본값
        help_text (str): 도움말 텍스트
        
    Returns:
        str: 입력된 텍스트
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 텍스트 입력 필드 렌더링
    input_value = st.text_input(
        display_label,
        key=key,
        placeholder=placeholder,
        disabled=disabled,
        value=value,
        help=help_text
    )
    
    # 필수 필드이고 값이 비어 있는 경우 경고 표시
    if required and not input_value and st.session_state.get(f"{key}_submitted", False):
        st.error(get_text("required_field", lang))
    
    return input_value

def render_number_input(label, key, min_value=0, max_value=None, step=1, lang="ko", required=False, disabled=False, value=0, help_text=""):
    """
    숫자 입력 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        key (str): 입력 필드의 고유 키
        min_value (int): 최소값
        max_value (int): 최대값
        step (int): 증가/감소 단계
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        value (int): 기본값
        help_text (str): 도움말 텍스트
        
    Returns:
        int: 입력된 숫자
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 숫자 입력 필드 렌더링
    input_value = st.number_input(
        display_label,
        min_value=min_value,
        max_value=max_value,
        step=step,
        key=key,
        disabled=disabled,
        value=value,
        help=help_text
    )
    
    return input_value

def render_selectbox(label, options, key, lang="ko", required=False, disabled=False, index=0, help_text=""):
    """
    선택 입력 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        options (list): 선택 옵션 목록
        key (str): 입력 필드의 고유 키
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        index (int): 기본 선택 인덱스
        help_text (str): 도움말 텍스트
        
    Returns:
        Any: 선택된 옵션
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 선택 입력 필드 렌더링
    selected_option = st.selectbox(
        display_label,
        options=options,
        key=key,
        disabled=disabled,
        index=index,
        help=help_text
    )
    
    # 필수 필드이고 값이 비어 있는 경우 경고 표시
    if required and not selected_option and st.session_state.get(f"{key}_submitted", False):
        st.error(get_text("required_field", lang))
    
    return selected_option

def render_date_input(label, key, lang="ko", required=False, disabled=False, value=None, help_text=""):
    """
    날짜 선택 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        key (str): 입력 필드의 고유 키
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        value (date): 기본 날짜(None인 경우 오늘 날짜)
        help_text (str): 도움말 텍스트
        
    Returns:
        date: 선택된 날짜
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 기본값이 None인 경우 오늘 날짜 사용
    if value is None:
        value = date.today()
    
    # 날짜 선택 필드 렌더링
    selected_date = st.date_input(
        display_label,
        value=value,
        key=key,
        disabled=disabled,
        help=help_text
    )
    
    return selected_date

def render_time_input(label, key, lang="ko", required=False, disabled=False, value=None, help_text=""):
    """
    시간 선택 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        key (str): 입력 필드의 고유 키
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        value (time): 기본 시간(None인 경우 현재 시간)
        help_text (str): 도움말 텍스트
        
    Returns:
        time: 선택된 시간
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 기본값이 None인 경우 현재 시간 사용
    if value is None:
        value = datetime.now().time()
    
    # 시간 선택 필드 렌더링
    selected_time = st.time_input(
        display_label,
        value=value,
        key=key,
        disabled=disabled,
        help=help_text
    )
    
    return selected_time

def render_file_uploader(label, key, type=["png", "jpg", "jpeg"], lang="ko", required=False, disabled=False, help_text=""):
    """
    파일 업로드 필드를 렌더링합니다.
    
    Args:
        label (str): 필드 레이블
        key (str): 입력 필드의 고유 키
        type (list): 허용되는 파일 유형 목록
        lang (str): 언어 코드 ('ko' 또는 'vi')
        required (bool): 필수 입력 여부
        disabled (bool): 비활성화 여부
        help_text (str): 도움말 텍스트
        
    Returns:
        bytes: 업로드된 파일 데이터
    """
    # 레이블에 필수 표시 추가
    display_label = f"{label} *" if required else label
    
    # 파일 업로드 필드 렌더링
    uploaded_file = st.file_uploader(
        display_label,
        type=type,
        key=key,
        disabled=disabled,
        help=help_text
    )
    
    # 필수 필드이고 파일이 업로드되지 않은 경우 경고 표시
    if required and not uploaded_file and st.session_state.get(f"{key}_submitted", False):
        st.error(get_text("required_file", lang))
    
    return uploaded_file

def render_error_message(message, lang="ko"):
    """
    오류 메시지를 렌더링합니다.
    
    Args:
        message (str): 오류 메시지
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 메시지는 직접 화면에 표시됩니다.
    """
    st.error(message)

def render_success_message(message, lang="ko"):
    """
    성공 메시지를 렌더링합니다.
    
    Args:
        message (str): 성공 메시지
        lang (str): 언어 코드 ('ko' 또는 'vi')
        
    Returns:
        None: 메시지는 직접 화면에 표시됩니다.
    """
    st.success(message)

def render_form_button(label, key, type="primary", lang="ko", disabled=False, help_text=""):
    """
    폼 버튼을 렌더링합니다.
    
    Args:
        label (str): 버튼 레이블
        key (str): 버튼의 고유 키
        type (str): 버튼 유형 ('primary' 또는 'secondary')
        lang (str): 언어 코드 ('ko' 또는 'vi')
        disabled (bool): 비활성화 여부
        help_text (str): 도움말 텍스트
        
    Returns:
        bool: 버튼 클릭 여부
    """
    # 버튼 유형에 따라 렌더링
    if type == "primary":
        return st.button(
            label,
            key=key,
            type="primary",
            disabled=disabled,
            help=help_text
        )
    else:
        return st.button(
            label,
            key=key,
            disabled=disabled,
            help=help_text
        ) 