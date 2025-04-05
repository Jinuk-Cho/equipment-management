from datetime import datetime
from utils.database import Database

class PlanService:
    def __init__(self):
        self.db = Database()
    
    # ... existing code ...
    
    def suspend_plan(self, plan_code: str, start_date: date, end_date: date, reason: str) -> bool:
        try:
            # 기존 정지 기간과 중복 체크
            query = """
                SELECT COUNT(*) 
                FROM plan_suspensions 
                WHERE plan_code = :plan_code 
                AND NOT (end_date < :start_date OR start_date > :end_date)
            """
            result = self.db.execute_query(
                query,
                {"plan_code": plan_code, "start_date": start_date, "end_date": end_date}
            )
            
            if result[0][0] > 0:
                raise ValueError("해당 기간에 이미 정지 계획이 존재합니다.")
            
            # 계획 상태 업데이트
            update_query = """
                UPDATE maintenance_plans 
                SET status = 'SUSPENDED',
                    updated_at = CURRENT_TIMESTAMP
                WHERE plan_code = :plan_code
            """
            self.db.execute_query(update_query, {"plan_code": plan_code})
            
            # 정지 정보 저장
            insert_query = """
                INSERT INTO plan_suspensions (
                    plan_code, start_date, end_date, reason, created_at
                ) VALUES (
                    :plan_code, :start_date, :end_date, :reason, CURRENT_TIMESTAMP
                )
            """
            self.db.execute_query(
                insert_query,
                {
                    "plan_code": plan_code,
                    "start_date": start_date,
                    "end_date": end_date,
                    "reason": reason
                }
            )
            
            return True
            
        except Exception as e:
            print(f"Error in suspend_plan: {str(e)}")
            return False 

    def get_suspended_plans(self):
        query = """
            SELECT 
                mp.plan_code,
                mp.equipment_number,
                ps.start_date,
                ps.end_date,
                ps.reason
            FROM maintenance_plans mp
            JOIN plan_suspensions ps ON mp.plan_code = ps.plan_code
            WHERE mp.status = 'SUSPENDED'
            AND ps.end_date >= CURRENT_DATE
            ORDER BY ps.start_date ASC
        """
        
        return self.db.execute_query(query) 