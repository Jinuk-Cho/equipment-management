import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
from components.language import get_text, _normalize_language_code

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
    # 언어 코드 표준화
    normalized_lang = _normalize_language_code(lang)
    
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
    
    # 기본값 설정 (언어 코드가 잘못된 경우 한국어 사용)
    worker_list = workers.get(normalized_lang, workers['ko'])
    
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
            '작업자': random.choice(worker_list)
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
            '작업자': random.choice(worker_list)
        })
    
    return pd.DataFrame(error_data), pd.DataFrame(parts_data)

class ReportsComponent:
    def __init__(self, lang=None):
        self.lang = lang if lang else 'kr'
        
    def render(self):
        """보고서 및 통계 페이지를 렌더링합니다."""
        # 언어 설정: 클래스의 lang 속성 우선 사용, 없으면 세션 상태에서 가져오기
        lang = self.lang
        if 'current_lang' in st.session_state:
            lang = st.session_state.current_lang
            
        st.title(get_report_text("reports_title", lang))
        
        # 탭 생성
        tabs = st.tabs([
            get_report_text("error_type_analysis", lang),
            get_report_text("parts_consumption", lang),
            get_report_text("worker_statistics", lang),
            get_report_text("downtime_analysis", lang)
        ])
        
        # 예시 데이터 생성
        error_data, parts_data = generate_sample_data(lang)
        
        # 오류 데이터 데이터프레임으로 변환
        df_errors = pd.DataFrame(error_data)
        df_errors['시간'] = df_errors['발생시간'].dt.hour
        df_errors['월'] = df_errors['발생시간'].dt.month
        
        # 부품 데이터 데이터프레임으로 변환
        df_parts = pd.DataFrame(parts_data)
        df_parts['월'] = df_parts['교체시간'].dt.month
        
        # 고장 유형 분석 탭
        with tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                # 오류 코드별 발생 횟수
                error_counts = df_errors['오류코드'].value_counts().reset_index()
                error_counts.columns = [get_report_text("error_code", lang), get_report_text("occurrences", lang)]
                
                fig_error_counts = px.bar(
                    error_counts,
                    x=get_report_text("error_code", lang),
                    y=get_report_text("occurrences", lang),
                    title=get_report_text("occurrences_by_error_code", lang)
                )
                st.plotly_chart(fig_error_counts, use_container_width=True)
            
            with col2:
                # 시간대별 고장 발생 추이
                hour_counts = df_errors['시간'].value_counts().reset_index()
                hour_counts.columns = [get_report_text("hour", lang), get_report_text("occurrences", lang)]
                hour_counts = hour_counts.sort_values(by=get_report_text("hour", lang))
                
                fig_hour_counts = px.line(
                    hour_counts,
                    x=get_report_text("hour", lang),
                    y=get_report_text("occurrences", lang),
                    markers=True,
                    title=get_report_text("error_trend_by_hour", lang)
                )
                st.plotly_chart(fig_hour_counts, use_container_width=True)
        
        # 부품 소모 현황 탭
        with tabs[1]:
            col1, col2 = st.columns(2)
            
            with col1:
                # 부품별 교체 횟수
                part_counts = df_parts['부품코드'].value_counts().reset_index()
                part_counts.columns = [get_report_text("part_code", lang), get_report_text("replacements", lang)]
                
                fig_part_counts = px.bar(
                    part_counts,
                    x=get_report_text("part_code", lang),
                    y=get_report_text("replacements", lang),
                    title=get_report_text("replacements_by_part", lang)
                )
                st.plotly_chart(fig_part_counts, use_container_width=True)
            
            with col2:
                # 부품별 교체 비율
                fig_part_pie = px.pie(
                    part_counts,
                    names=get_report_text("part_code", lang),
                    values=get_report_text("replacements", lang),
                    title=get_report_text("replacement_ratio_by_part", lang)
                )
                st.plotly_chart(fig_part_pie, use_container_width=True)
            
            # 월별 부품 교체 추이
            monthly_parts = df_parts.groupby('월').size().reset_index()
            monthly_parts.columns = [get_report_text("month", lang), get_report_text("replacements", lang)]
            
            fig_monthly_parts = px.line(
                monthly_parts,
                x=get_report_text("month", lang),
                y=get_report_text("replacements", lang),
                markers=True,
                title=get_report_text("monthly_parts_trend", lang)
            )
            st.plotly_chart(fig_monthly_parts, use_container_width=True)
        
        # 작업자별 통계 탭
        with tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                # 작업자별 처리 건수
                worker_counts = df_errors['작업자'].value_counts().reset_index()
                worker_counts.columns = [get_report_text("worker", lang), get_report_text("repairs", lang)]
                
                fig_worker_counts = px.bar(
                    worker_counts,
                    x=get_report_text("worker", lang),
                    y=get_report_text("repairs", lang),
                    title=get_report_text("repairs_by_worker", lang)
                )
                st.plotly_chart(fig_worker_counts, use_container_width=True)
            
            with col2:
                # 작업자별 평균 수리 시간
                worker_repair_times = df_errors.groupby('작업자')['수리시간'].mean().reset_index()
                worker_repair_times.columns = [get_report_text("worker", lang), get_report_text("avg_repair_time", lang)]
                
                fig_worker_times = px.bar(
                    worker_repair_times,
                    x=get_report_text("worker", lang),
                    y=get_report_text("avg_repair_time", lang),
                    title=get_report_text("avg_repair_time_by_worker", lang)
                )
                st.plotly_chart(fig_worker_times, use_container_width=True)
        
        # 다운타임 분석 탭
        with tabs[3]:
            col1, col2 = st.columns(2)
            
            with col1:
                # 설비별 다운타임
                equipment_downtime = df_errors.groupby('설비번호')['수리시간'].sum().reset_index()
                equipment_downtime.columns = [get_report_text("equipment_number", lang), get_report_text("total_downtime", lang)]
                
                fig_equipment_downtime = px.bar(
                    equipment_downtime,
                    x=get_report_text("equipment_number", lang),
                    y=get_report_text("total_downtime", lang),
                    title=get_report_text("downtime_by_equipment", lang)
                )
                st.plotly_chart(fig_equipment_downtime, use_container_width=True)
            
            with col2:
                # 오류 코드별 평균 수리 시간
                error_repair_times = df_errors.groupby('오류코드')['수리시간'].mean().reset_index()
                error_repair_times.columns = [get_report_text("error_code", lang), get_report_text("avg_repair_time", lang)]
                
                fig_error_times = px.bar(
                    error_repair_times,
                    x=get_report_text("error_code", lang),
                    y=get_report_text("avg_repair_time", lang),
                    title=get_report_text("avg_repair_time_by_error", lang)
                )
                st.plotly_chart(fig_error_times, use_container_width=True)
        
        # 통계 요약 (아래쪽에 표시)
        st.subheader(get_report_text("statistics_summary", lang))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                get_report_text("average_repair_time", lang),
                f"{df_errors['수리시간'].mean():.1f} {get_report_text('minutes', lang)}"
            )
        
        with col2:
            st.metric(
                get_report_text("max_repair_time", lang),
                f"{df_errors['수리시간'].max()} {get_report_text('minutes', lang)}"
            )
        
        with col3:
            st.metric(
                get_report_text("total_downtime", lang),
                f"{df_errors['수리시간'].sum()} {get_report_text('minutes', lang)}"
            )

# 원래 함수는 주석 처리합니다
# def show_reports(lang='ko'):
#     """보고서 페이지를 표시합니다."""
#     st.title(get_report_text("reports_title", lang))
#     
#     # 탭 생성
#     tabs = st.tabs([
#         get_report_text("error_type_analysis", lang),
#         get_report_text("parts_consumption", lang),
#         get_report_text("worker_statistics", lang),
#         get_report_text("downtime_analysis", lang)
#     ])
#     
#     // ... rest of the original function ... 