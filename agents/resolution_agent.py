from tools.action_executor import ActionExecutorTool
from models.schemas import Ticket

class ResolutionAgent:
    def __init__(self):
        self.executor = ActionExecutorTool()
    def resolve(self, ticket: Ticket) -> Ticket:
        print("✨ [Resolution Agent] Attempting automated fix...")
        action_res = self.executor.execute('apply_fix', {'category': ticket.category})
        ticket.resolution = {'method': 'automated', 'actions_taken': [action_res], 'resolution_summary': {'employee_message': 'Automated troubleshooting actions have been applied.'}, 'success': True}
        ticket.status = 'resolved'
        ticket.add_action('resolution_agent', 'resolve', 'Issue resolved via automated actions')
        return ticket
