import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random
from components.language import get_text
from services.plan_service import PlanService
from utils.supabase_client import get_equipment_list, get_error_history, get_parts_replacement

class DashboardComponent:
    def __init__(self):
        self.plan_service = PlanService()

    def render(self):
        st.title(get_text("dashboard", st.session_state.language))
        
        # 예시 데이터 생성
        equipment_list = generate_equipment_data(st.session_state.language)
        error_history = generate_error_data(datetime.now() - timedelta(days=30), datetime.now())
        parts_history = generate_parts_data(datetime.now() - timedelta(days=30), datetime.now())
        
        # 데이터프레임 변환
        df_equipment = pd.DataFrame(equipment_list)
        df_errors = pd.DataFrame(error_history)
        df_parts = pd.DataFrame(parts_history)
        
        # 2x2 그리드 레이아웃
        col1, col2 = st.columns(2)
        
        # 첫 번째 열
        with col1:
            # 설비 상태 요약
            if not df_equipment.empty:
                # 상태별 카운트
                status_counts = df_equipment['status'].value_counts()
                
                # 설비 상태 요약 지표 표시
                st.subheader(get_text("equipment_status_summary", st.session_state.language))
                
                # 상태별 개수 표시
                status_cols = st.columns(3)
                with status_cols[0]:
                    error_count = status_counts.get(get_text("error", st.session_state.language), 0)
                    st.metric("고장", f"{error_count}대", delta_color="inverse")
                    if error_count > 0 and st.button("상세보기", key="view_error_details"):
                        st.session_state.view_equipment_status = "error"
                        st.session_state.current_page = 'equipment_status_detail'
                        st.rerun()
                    
                with status_cols[1]:
                    pm_count = status_counts.get("설비 PM", 0)
                    st.metric("설비 PM", f"{pm_count}대", delta_color="off")
                    if pm_count > 0 and st.button("상세보기", key="view_pm_details"):
                        st.session_state.view_equipment_status = "pm"
                        st.session_state.current_page = 'equipment_status_detail'
                        st.rerun()
                    
                with status_cols[2]:
                    model_change_count = status_counts.get("모델 변경", 0)
                    st.metric("모델 변경", f"{model_change_count}대", delta_color="off")
                    if model_change_count > 0 and st.button("상세보기", key="view_model_change_details"):
                        st.session_state.view_equipment_status = "model_change"
                        st.session_state.current_page = 'equipment_status_detail'
                        st.rerun()
                
                # 파이 차트로 시각화
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title=get_text("equipment_status_distribution", st.session_state.language),
                    height=300
                )
                fig_status.update_layout(margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_status, use_container_width=True)
            
            # 고장 유형별 분포
            if not df_errors.empty:
                error_types = df_errors['error_code'].value_counts()
                fig_error_types = px.bar(
                    x=error_types.index,
                    y=error_types.values,
                    title=get_text("error_distribution", st.session_state.language),
                    labels={
                        'x': get_text("error_code", st.session_state.language), 
                        'y': get_text("count", st.session_state.language)
                    },
                    height=300
                )
                fig_error_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_error_types, use_container_width=True)
        
        # 두 번째 열
        with col2:
            # 시간별 고장 건수
            if not df_errors.empty:
                df_errors['date'] = pd.to_datetime(df_errors['timestamp']).dt.date
                daily_errors = df_errors.groupby('date').size().reset_index(name='count')
                fig_errors = px.line(
                    daily_errors,
                    x='date',
                    y='count',
                    title=get_text("daily_errors", st.session_state.language),
                    labels={
                        'date': get_text("date", st.session_state.language), 
                        'count': get_text("count", st.session_state.language)
                    },
                    height=300
                )
                fig_errors.update_layout(margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_errors, use_container_width=True)
            
            # 부품별 교체 횟수
            if not df_parts.empty:
                parts_counts = df_parts['part_code'].value_counts()
                fig_parts_types = px.bar(
                    x=parts_counts.index,
                    y=parts_counts.values,
                    title=get_text("parts_replacement", st.session_state.language),
                    labels={
                        'x': get_text("part_code", st.session_state.language), 
                        'y': get_text("count", st.session_state.language)
                    },
                    height=300
                )
                fig_parts_types.update_layout(margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_parts_types, use_container_width=True)
        
        # 통계 요약 - 하단에 배치
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                get_text("average_repair_time", st.session_state.language),
                f"{df_errors['repair_time'].mean():.1f} {get_text('minutes', st.session_state.language)}"
            )
        with col2:
            st.metric(
                get_text("max_repair_time", st.session_state.language),
                f"{df_errors['repair_time'].max()} {get_text('minutes', st.session_state.language)}"
            )
        with col3:
            st.metric(
                get_text("total_downtime", st.session_state.language),
                f"{df_errors['repair_time'].sum()} {get_text('minutes', st.session_state.language)}"
            )

    def render_suspended_plans(self):
        st.subheader(get_text("plan_suspension", st.session_state.language))
        
        suspended_plans = self.plan_service.get_suspended_plans()
        
        if not suspended_plans:
            st.info(get_text("no_suspended_plans", st.session_state.language))
            return
            
        for plan in suspended_plans:
            with st.container():
                col1, col2 = st.columns([2,1])
                with col1:
                    st.markdown(f"**{plan['plan_code']}** - {plan['equipment_number']}")
                    st.markdown(f"{get_text('suspension_period', st.session_state.language)}: "
                              f"{plan['start_date']} ~ {plan['end_date']}")
                    st.markdown(f"{get_text('suspension_reason', st.session_state.language)}: {plan['reason']}")
                with col2:
                    if st.button(get_text("resume_plan", st.session_state.language), 
                               key=f"resume_{plan['plan_code']}", type="primary"):
                        if self.plan_service.resume_plan(plan['plan_code']):
                            st.success(get_text("plan_resumed", st.session_state.language))
                            st.rerun()
                st.divider()

    def render_equipment_status(self):
        equipment_list = get_equipment_list()
        if equipment_list:
            df = pd.DataFrame(equipment_list)
            fig = px.pie(df, names='status', title=get_text("equipment_status", st.session_state.language))
            st.plotly_chart(fig)

    def render_error_stats(self):
        error_history = get_error_history()
        if error_history:
            df = pd.DataFrame(error_history)
            fig = px.bar(df, x='error_code', title=get_text("error_distribution", st.session_state.language))
            st.plotly_chart(fig)

    def render_parts_stats(self):
        parts_data = get_parts_replacement()
        if parts_data:
            df = pd.DataFrame(parts_data)
            fig = px.bar(df, x='part_name', title=get_text("parts_replacement", st.session_state.language))
            st.plotly_chart(fig)

def generate_equipment_data(lang='ko'):
    """설비 데이터 예시를 생성합니다."""
    equipment_data = [
        {
            'equipment_number': 'EQ001',
            'building': 'A동',
            'equipment_type': '프레스',
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ002',
            'building': 'B동',
            'equipment_type': '컨베이어',
            'status': '설비 PM'
        },
        {
            'equipment_number': 'EQ003',
            'building': 'A동',
            'equipment_type': '로봇',
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ004',
            'building': 'C동',
            'equipment_type': '프레스',
            'status': get_text("error", lang)
        },
        {
            'equipment_number': 'EQ005',
            'building': 'B동',
            'equipment_type': '로봇',
            'status': '모델 변경'
        },
        {
            'equipment_number': 'EQ006',
            'building': 'A동',
            'equipment_type': '컨베이어',
            'status': get_text("normal", lang)
        },
        {
            'equipment_number': 'EQ007',
            'building': 'C동',
            'equipment_type': '로봇',
            'status': get_text("error", lang)
        },
        {
            'equipment_number': 'EQ008',
            'building': 'B동',
            'equipment_type': '프레스',
            'status': '설비 PM'
        }
    ]
    return equipment_data

def generate_error_data(start_date, end_date):
    """고장 데이터 예시를 생성합니다."""
    error_data = []
    for _ in range(50):
        timestamp = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        error_data.append({
            'timestamp': timestamp,
            'equipment_number': f'EQ00{random.randint(1, 5)}',
            'error_code': f'E00{random.randint(1, 5)}',
            'repair_time': random.randint(10, 120)
        })
    return error_data

def generate_parts_data(start_date, end_date):
    """부품 교체 데이터 예시를 생성합니다."""
    parts_data = []
    for _ in range(30):
        timestamp = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        parts_data.append({
            'timestamp': timestamp,
            'equipment_number': f'EQ00{random.randint(1, 5)}',
            'part_code': f'P00{random.randint(1, 4)}'
        })
    return parts_data 