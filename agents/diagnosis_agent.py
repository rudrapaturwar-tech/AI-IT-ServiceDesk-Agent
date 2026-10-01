from tools.system_checker import SystemCheckerTool
from models.schemas import Ticket

class DiagnosisAgent:
    def __init__(self):
        self.checker = SystemCheckerTool()
    def diagnose(self, ticket: Ticket) -> Ticket:
        print("🔧 [Diagnosis Agent] Checking system health...")
        affected = self.checker.get_affected_systems(ticket.category)
        is_sys_issue = any(s['status'] != 'operational' for s in affected)
        ticket.diagnosis_results = {'affected_systems': affected, 'root_cause_analysis': {'is_system_issue': is_sys_issue}}
        ticket.add_action('diagnosis_agent', 'diagnose', f"System-wide issue: {is_sys_issue}")
        return ticket
