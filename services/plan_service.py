from datetime import datetime, date
import random

class PlanService:
    def __init__(self):
        pass
    
    def suspend_plan(self, plan_code: str, start_date: str, end_date: str, reason: str) -> bool:
        """계획을 정지 상태로 변경합니다."""
        # 실제 데이터베이스 연동 없이 항상 성공으로 처리
        return True

    def resume_plan(self, plan_code: str) -> bool:
        """정지된 계획을 다시 활성화합니다."""
        # 실제 데이터베이스 연동 없이 항상 성공으로 처리
        return True

    def get_suspended_plans(self):
        """정지된 계획 목록을 반환합니다."""
        # 예시 데이터 생성
        plans = []
        if random.random() > 0.5:  # 랜덤하게 데이터 존재 여부 결정
            plans = [
                {
                    'plan_code': 'P2023001',
                    'equipment_number': 'EQ001',
                    'start_date': '2023-07-01',
                    'end_date': '2023-07-15',
                    'reason': '연간 점검'
                },
                {
                    'plan_code': 'P2023002',
                    'equipment_number': 'EQ003',
                    'start_date': '2023-07-10',
                    'end_date': '2023-07-20',
                    'reason': '부품 교체'
                }
            ]
        return plans
        
    def get_suspension_history(self):
        """정지 이력을 반환합니다."""
        # 예시 데이터 생성
        today = date.today()
        history = [
            {
                'plan_code': 'P2022001',
                'equipment_number': 'EQ002',
                'start_date': '2022-05-15',
                'end_date': '2022-05-25',
                'reason': '정기 점검',
                'status': 'COMPLETED'
            },
            {
                'plan_code': 'P2022003',
                'equipment_number': 'EQ001',
                'start_date': '2022-08-10',
                'end_date': '2022-08-20',
                'reason': '설비 업그레이드',
                'status': 'COMPLETED'
            },
            {
                'plan_code': 'P2023004',
                'equipment_number': 'EQ005',
                'start_date': '2023-01-05',
                'end_date': '2023-01-15',
                'reason': '부품 교체',
                'status': 'COMPLETED'
            }
        ]
        return history 