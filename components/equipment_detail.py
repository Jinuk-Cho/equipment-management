import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show_equipment_detail():
    """장비 상세 정보를 표시합니다."""
    st.title("설비 상세 정보")
    
    # 예시 데이터 생성
    equipment_list = {
        'equipment_number': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
        'building': ['A동', 'B동', 'A동', 'C동', 'B동'],
        'equipment_type': ['프레스', '컨베이어', '로봇', '프레스', '로봇'],
        'status': ['정상', '점검중', '정상', '고장', '정상'],
        'last_maintenance': [
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=1)
        ]
    }
    
    # 설비 선택
    df_equipment = pd.DataFrame(equipment_list)
    selected_equipment = st.selectbox(
        "설비 선택",
        options=df_equipment['equipment_number'].tolist(),
        format_func=lambda x: f"{x} ({df_equipment[df_equipment['equipment_number']==x]['equipment_type'].iloc[0]})"
    )
    
    if selected_equipment:
        equipment_info = df_equipment[df_equipment['equipment_number'] == selected_equipment].iloc[0]
        
        # 설비 기본 정보
        st.subheader("기본 정보")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("설비 번호", equipment_info['equipment_number'])
        with col2:
            st.metric("설비 유형", equipment_info['equipment_type'])
        with col3:
            st.metric("설치 위치", equipment_info['building'])
            
        # 상태 정보
        st.subheader("상태 정보")
        status_color = {
            '정상': 'green',
            '점검중': 'orange',
            '고장': 'red'
        }
        
        st.markdown(f"""
        <div style='padding: 1rem; border-radius: 0.5rem; background-color: {status_color.get(equipment_info['status'], 'gray')}25;'>
            <h3 style='color: {status_color.get(equipment_info['status'], 'gray')}; margin: 0;'>
                현재 상태: {equipment_info['status']}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 정비 이력
        st.subheader("정비 이력")
        maintenance_history = {
            'date': [
                datetime.now() - timedelta(days=x) 
                for x in [1, 5, 10, 15, 20]
            ],
            'type': ['정기점검', '부품교체', '정기점검', '고장수리', '정기점검'],
            'description': [
                '월간 정기점검 완료',
                '베어링 교체',
                '월간 정기점검 완료',
                '모터 과열 수리',
                '월간 정기점검 완료'
            ],
            'worker': ['김철수', '박영희', '김철수', '이영수', '김철수']
        }
        
        df_history = pd.DataFrame(maintenance_history)
        st.dataframe(
            df_history,
            column_config={
                "date": st.column_config.DatetimeColumn(
                    "작업일시",
                    format="YYYY-MM-DD HH:mm"
                ),
                "type": "작업유형",
                "description": "작업내용",
                "worker": "작업자"
            }
        )
        
        # 부품 교체 이력
        st.subheader("부품 교체 이력")
        parts_history = {
            'date': [
                datetime.now() - timedelta(days=x)
                for x in [5, 15, 30]
            ],
            'part_code': ['P001', 'P002', 'P003'],
            'part_name': ['베어링', '모터', '센서'],
            'quantity': [2, 1, 3],
            'worker': ['박영희', '이영수', '박영희']
        }
        
        df_parts = pd.DataFrame(parts_history)
        st.dataframe(
            df_parts,
            column_config={
                "date": st.column_config.DatetimeColumn(
                    "교체일시",
                    format="YYYY-MM-DD HH:mm"
                ),
                "part_code": "부품코드",
                "part_name": "부품명",
                "quantity": "수량",
                "worker": "작업자"
            }
        ) 