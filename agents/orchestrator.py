from models.schemas import Ticket, Priority
from agents.triage_agent import TriageAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.troubleshoot_agent import TroubleshootAgent
from agents.resolution_agent import ResolutionAgent
from agents.escalation_agent import EscalationAgent
import uuid
from datetime import datetime

class Orchestrator:
    def __init__(self):
        self.triage = TriageAgent()
        self.knowledge = KnowledgeAgent()
        self.diagnosis = DiagnosisAgent()
        self.troubleshoot = TroubleshootAgent()
        self.resolution = ResolutionAgent()
        self.escalation = EscalationAgent()
        
    def process_ticket(self, employee_name, issue_description, employee_email='', department=''):
        ticket = Ticket(
            ticket_id=f"TK-{uuid.uuid4().hex[:6].upper()}",
            employee_name=employee_name,
            employee_email=employee_email,
            department=department,
            issue_description=issue_description
        )
        print(f"\n{'='*55}\n🎫 TICKET {ticket.ticket_id}: {employee_name}\n📝 Issue: {issue_description}\n{'='*55}")
        
        # 1. Triage
        ticket = self.triage.analyze(ticket)
        
        # 2. Dynamic Routing based on Challenge Requirement
        cat = ticket.category
        if cat == 'security_incident':
            ticket = self.diagnosis.diagnose(ticket)
            ticket = self.escalation.escalate(ticket, 'Security incident requires immediate human containment')
        elif cat == 'hardware_issue':
            ticket = self.knowledge.investigate(ticket)
            ticket = self.diagnosis.diagnose(ticket)
            ticket = self.escalation.escalate(ticket, 'Physical hardware replacement or inspection needed')
        elif cat == 'password_reset' or cat == 'software_install':
            ticket = self.knowledge.investigate(ticket)
            ticket = self.resolution.resolve(ticket)
        else: # network, email, performance
            ticket = self.diagnosis.diagnose(ticket)
            if ticket.diagnosis_results.get('root_cause_analysis', {}).get('is_system_issue'):
                ticket = self.escalation.escalate(ticket, 'Infrastructure / Service Outage detected')
            else:
                ticket = self.knowledge.investigate(ticket)
                ticket = self.troubleshoot.troubleshoot(ticket)
                ticket = self.resolution.resolve(ticket)
                
        print(f"\n📊 FINAL STATUS: {ticket.status.upper()}")
        for a in ticket.agent_actions:
            print(f"   ➔ [{a['agent']}]: {a['result']}")
        print(f"{'='*55}")
        return ticket
