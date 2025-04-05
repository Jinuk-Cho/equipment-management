class NotificationService:
    def __init__(self):
        self.db = Database()
    
    # ... existing code ...
    
    def create_suspension_notification(self, plan_code: str, start_date: date, end_date: date):
        message = f"계획 {plan_code}가 {start_date}부터 {end_date}까지 정지되었습니다."
        
        query = """
            INSERT INTO notifications (
                notification_type, target_user, message, created_at, read_status
            ) VALUES (
                'PLAN_SUSPENDED', 
                (SELECT created_by FROM maintenance_plans WHERE plan_code = :plan_code),
                :message,
                CURRENT_TIMESTAMP,
                false
            )
        """
        
        self.db.execute_query(
            query,
            {"plan_code": plan_code, "message": message}
        ) 