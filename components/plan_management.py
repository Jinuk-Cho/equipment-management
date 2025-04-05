from components.plan_suspension import PlanSuspensionComponent

class PlanManagementComponent:
    def __init__(self):
        self.plan_service = PlanService()
        self.suspension_component = PlanSuspensionComponent()
    
    def render(self):
        st.title("계획 관리")
        
        # ... existing code ...
        
        if selected_plan:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("계획 수정"):
                    self.show_edit_form(selected_plan)
            
            with col2:
                if st.button("계획 정지"):
                    if self.suspension_component.render(selected_plan["plan_code"]):
                        st.rerun()
            
            with col3:
                if st.button("계획 삭제"):
                    self.delete_plan(selected_plan["plan_code"]) 