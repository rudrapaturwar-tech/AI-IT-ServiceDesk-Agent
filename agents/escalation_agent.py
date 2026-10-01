from tools.email_notifier import EmailNotifierTool
from models.schemas import Ticket

class EscalationAgent:
    def __init__(self):
        self.notifier = EmailNotifierTool()
    def escalate(self, ticket: Ticket, reason: str = '') -> Ticket:
        print("🚨 [Escalation Agent] Escalating to human IT...")
        team = 'SOC Security Team' if ticket.category == 'security_incident' else 'Hardware Team' if ticket.category == 'hardware_issue' else 'L2 IT Support'
        ticket.escalation_info = {'escalate_to': team, 'reason': reason or 'Requires human assistance'}
        ticket.status = 'escalated'
        self.notifier.notify_it_team(ticket.ticket_id, ticket.priority.value, reason)
        ticket.add_action('escalation_agent', 'escalate', f"Escalated to {team}")
        return ticket
