import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
from components.language import get_text

# 보고서 페이지 텍스트
REPORTS_TEXTS = {
    "reports_title": {
        "ko": "보고서 및 통계",
        "vi": "Báo cáo và thống kê"
    },
    "error_type_analysis": {
        "ko": "고장 유형 분석",
        "vi": "Phân tích loại lỗi"
    },
    "parts_consumption": {
        "ko": "부품 소모 현황",
        "vi": "Tình trạng tiêu thụ linh kiện"
    },
    "worker_statistics": {
        "ko": "작업자별 통계",
        "vi": "Thống kê theo người thực hiện"
    },
    "downtime_analysis": {
        "ko": "다운타임 분석",
        "vi": "Phân tích thời gian ngừng máy"
    },
    "occurrences_by_error_code": {
        "ko": "오류 코드별 발생 횟수",
        "vi": "Số lần xuất hiện theo mã lỗi"
    },
    "error_trend_by_hour": {
        "ko": "시간대별 고장 발생 추이",
        "vi": "Xu hướng xuất hiện lỗi theo giờ"
    },
    "replacements_by_part": {
        "ko": "부품별 교체 횟수",
        "vi": "Số lần thay thế theo linh kiện"
    },
    "replacement_ratio_by_part": {
        "ko": "부품별 교체 비율",
        "vi": "Tỷ lệ thay thế theo linh kiện"
    },
    "monthly_parts_trend": {
        "ko": "월별 부품 교체 추이",
        "vi": "Xu hướng thay thế linh kiện theo tháng"
    },
    "repairs_by_worker": {
        "ko": "작업자별 처리 건수",
        "vi": "Số lượng xử lý theo người thực hiện"
    },
    "avg_repair_time_by_worker": {
        "ko": "작업자별 평균 수리 시간",
        "vi": "Thời gian sửa chữa trung bình theo người thực hiện"
    },
    "downtime_by_equipment": {
        "ko": "설비별 다운타임",
        "vi": "Thời gian ngừng máy theo thiết bị"
    },
    "avg_repair_time_by_error": {
        "ko": "오류 코드별 평균 수리 시간",
        "vi": "Thời gian sửa chữa trung bình theo mã lỗi"
    },
    "statistics_summary": {
        "ko": "통계 요약",
        "vi": "Tóm tắt thống kê"
    },
    "error_code": {
        "ko": "오류 코드",
        "vi": "Mã lỗi"
    },
    "occurrences": {
        "ko": "발생 횟수",
        "vi": "Số lần xuất hiện"
    },
    "hour": {
        "ko": "시간",
        "vi": "Giờ"
    },
    "part_code": {
        "ko": "부품 코드",
        "vi": "Mã linh kiện"
    },
    "replacements": {
        "ko": "교체 횟수",
        "vi": "Số lần thay thế"
    },
    "month": {
        "ko": "월",
        "vi": "Tháng"
    },
    "worker": {
        "ko": "작업자",
        "vi": "Người thực hiện"
    },
    "repairs": {
        "ko": "처리 건수",
        "vi": "Số lượng xử lý"
    },
    "avg_repair_time": {
        "ko": "평균 수리 시간 (분)",
        "vi": "Thời gian sửa chữa trung bình (phút)"
    },
    "equipment_number": {
        "ko": "설비 번호",
        "vi": "Số thiết bị"
    },
    "total_downtime": {
        "ko": "총 다운타임 (분)",
        "vi": "Tổng thời gian ngừng máy (phút)"
    },
    "average_repair_time": {
        "ko": "평균 수리 시간",
        "vi": "Thời gian sửa chữa trung bình"
    },
    "max_repair_time": {
        "ko": "최대 수리 시간",
        "vi": "Thời gian sửa chữa tối đa"
    },
    "minutes": {
        "ko": "분",
        "vi": "phút"
    }
}

def get_report_text(key, lang):
    """보고서 페이지 전용 텍스트를 가져옵니다."""
    if key in REPORTS_TEXTS:
        return REPORTS_TEXTS[key].get(lang, REPORTS_TEXTS[key]['ko'])
    return f"[{key}]"

def generate_sample_data(lang='ko'):
    """예시 데이터를 생성합니다."""
    # 현재 날짜를 기준으로 30일 전부터의 데이터 생성
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # 오류 이력 데이터
    error_codes = ['E001', 'E002', 'E003', 'E004', 'E005']
    equipment_numbers = ['EQ001', 'EQ002', 'EQ003', 'EQ004']
    
    workers = {
        'ko': ['김철수', '이영희', '박민수', '정지원'],
        'vi': ['Kim Cheolsu', 'Lee Younghee', 'Park Minsu', 'Jung Jiwon']
    }
    
    field_names = {
        'ko': {
            'occurrence_time': '발생시간',
            'equipment_number': '설비번호',
            'error_code': '오류코드',
            'repair_time': '수리시간',
            'worker': '작업자',
            'replacement_time': '교체시간',
            'part_code': '부품코드',
            'hour': '시간',
            'month': '월'
        },
        'vi': {
            'occurrence_time': '발생시간',
            'equipment_number': '설비번호',
            'error_code': '오류코드',
            'repair_time': '수리시간',
            'worker': '작업자',
            'replacement_time': '교체시간',
            'part_code': '부품코드',
            'hour': '시간',
            'month': '월'
        }
    }
    
    # 언어에 관계없이 데이터 처리를 위해 내부 필드명은 동일하게 유지
    error_data = []
    for _ in range(100):  # 100개의 오류 데이터 생성
        error_time = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        error_data.append({
            '발생시간': error_time,
            '설비번호': random.choice(equipment_numbers),
            '오류코드': random.choice(error_codes),
            '수리시간': random.randint(10, 120),
            '작업자': random.choice(workers[lang])
        })
    
    # 부품 교체 데이터
    part_codes = ['P001', 'P002', 'P003', 'P004']
    
    parts_data = []
    for _ in range(50):  # 50개의 부품 교체 데이터 생성
        replacement_time = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        parts_data.append({
            '교체시간': replacement_time,
            '설비번호': random.choice(equipment_numbers),
            '부품코드': random.choice(part_codes),
            '작업자': random.choice(workers[lang])
        })
    
    return pd.DataFrame(error_data), pd.DataFrame(parts_data)

def show_reports(lang='ko'):
    """보고서 및 통계 페이지를 표시합니다."""
    st.title(get_report_text("reports_title", lang))
    
    # 예시 데이터 생성
    error_history, parts_history = generate_sample_data(lang)
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        get_report_text("error_type_analysis", lang),
        get_report_text("parts_consumption", lang),
        get_report_text("worker_statistics", lang),
        get_report_text("downtime_analysis", lang)
    ])
    
    # 고장 유형 분석
    with tab1:
        st.subheader(get_report_text("occurrences_by_error_code", lang))
        error_counts = error_history['오류코드'].value_counts()
        
        fig = px.bar(
            x=error_counts.index,
            y=error_counts.values,
            labels={
                'x': get_report_text("error_code", lang), 
                'y': get_report_text("occurrences", lang)
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 시간대별 고장 발생 추이
        error_history['시간'] = pd.to_datetime(error_history['발생시간']).dt.hour
        hourly_errors = error_history['시간'].value_counts().sort_index()
        
        fig = px.line(
            x=hourly_errors.index,
            y=hourly_errors.values,
            labels={
                'x': get_report_text("hour", lang), 
                'y': get_report_text("occurrences", lang)
            },
            title=get_report_text("error_trend_by_hour", lang)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 부품 소모 현황
    with tab2:
        st.subheader(get_report_text("replacements_by_part", lang))
        parts_counts = parts_history['부품코드'].value_counts()
        
        fig = px.pie(
            values=parts_counts.values,
            names=parts_counts.index,
            title=get_report_text("replacement_ratio_by_part", lang)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 월별 부품 교체 추이
        parts_history['월'] = pd.to_datetime(parts_history['교체시간']).dt.strftime('%Y-%m')
        monthly_parts = parts_history.groupby('월')['부품코드'].count()
        
        fig = px.line(
            x=monthly_parts.index,
            y=monthly_parts.values,
            labels={
                'x': get_report_text("month", lang), 
                'y': get_report_text("replacements", lang)
            },
            title=get_report_text("monthly_parts_trend", lang)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 작업자별 통계
    with tab3:
        st.subheader(get_report_text("repairs_by_worker", lang))
        worker_counts = error_history['작업자'].value_counts()
        
        fig = px.bar(
            x=worker_counts.index,
            y=worker_counts.values,
            labels={
                'x': get_report_text("worker", lang), 
                'y': get_report_text("repairs", lang)
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 작업자별 평균 수리 시간
        worker_times = error_history.groupby('작업자')['수리시간'].mean()
        
        fig = px.bar(
            x=worker_times.index,
            y=worker_times.values,
            labels={
                'x': get_report_text("worker", lang), 
                'y': get_report_text("avg_repair_time", lang)
            },
            title=get_report_text("avg_repair_time_by_worker", lang)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 다운타임 분석
    with tab4:
        st.subheader(get_report_text("downtime_by_equipment", lang))
        equipment_downtime = error_history.groupby('설비번호')['수리시간'].sum()
        
        fig = px.bar(
            x=equipment_downtime.index,
            y=equipment_downtime.values,
            labels={
                'x': get_report_text("equipment_number", lang), 
                'y': get_report_text("total_downtime", lang)
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 오류 코드별 평균 수리 시간
        error_repair_time = error_history.groupby('오류코드')['수리시간'].mean()
        
        fig = px.bar(
            x=error_repair_time.index,
            y=error_repair_time.values,
            labels={
                'x': get_report_text("error_code", lang), 
                'y': get_report_text("avg_repair_time", lang)
            },
            title=get_report_text("avg_repair_time_by_error", lang)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 통계 요약
        st.subheader(get_report_text("statistics_summary", lang))
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                get_report_text("average_repair_time", lang),
                f"{error_history['수리시간'].mean():.1f} {get_report_text('minutes', lang)}"
            )
        with col2:
            st.metric(
                get_report_text("max_repair_time", lang),
                f"{error_history['수리시간'].max()} {get_report_text('minutes', lang)}"
            )
        with col3:
            st.metric(
                get_report_text("total_downtime", lang),
                f"{error_history['수리시간'].sum()} {get_report_text('minutes', lang)}"
            ) 