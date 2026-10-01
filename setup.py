import os
import json

print("🚀 Creating all project folders and files...")

# 1. Create Directories
directories = ['agents', 'tools', 'data', 'models', 'ui', 'tests']
for d in directories:
    os.makedirs(d, exist_ok=True)
    init_file = os.path.join(d, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('')

# 2. requirements.txt
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write("""openai==1.75.0
langchain==0.3.25
langchain-openai==0.3.18
langchain-community==0.3.24
python-dotenv==1.1.0
streamlit==1.45.1
pydantic==2.11.3
rich==14.0.0
""")

# 3. .env (if not exists)
if not os.path.exists('.env'):
    with open('.env', 'w', encoding='utf-8') as f:
        f.write("""OPENAI_API_KEY=sk-your-openai-key-here
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.1
""")

# 4. config.py
with open('config.py', 'w', encoding='utf-8') as f:
    f.write('''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))
    
    CATEGORIES = {
        "password_reset": {"keywords": ["password", "login", "locked out", "forgot password", "reset password", "credentials"], "priority": "medium", "auto_resolvable": True},
        "network_issue": {"keywords": ["internet", "wifi", "network", "vpn", "connection", "disconnected", "dns"], "priority": "high", "auto_resolvable": True},
        "software_install": {"keywords": ["install", "software", "application", "update", "license", "download"], "priority": "low", "auto_resolvable": True},
        "hardware_issue": {"keywords": ["monitor", "keyboard", "mouse", "printer", "laptop", "screen", "battery", "charger"], "priority": "medium", "auto_resolvable": False},
        "email_issue": {"keywords": ["email", "outlook", "calendar", "teams", "mailbox", "spam"], "priority": "medium", "auto_resolvable": True},
        "security_incident": {"keywords": ["virus", "malware", "hack", "breach", "phishing", "suspicious", "ransomware"], "priority": "critical", "auto_resolvable": False},
        "performance_issue": {"keywords": ["slow", "freeze", "crash", "blue screen", "hang", "lag", "cpu", "memory"], "priority": "medium", "auto_resolvable": True},
        "access_request": {"keywords": ["access", "permission", "role", "share", "folder", "drive", "privilege"], "priority": "medium", "auto_resolvable": False}
    }
''')

# 5. models/schemas.py
with open('models/schemas.py', 'w', encoding='utf-8') as f:
    f.write('''from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TicketStatus(str, Enum):
    NEW = "new"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    TROUBLESHOOTING = "troubleshooting"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class Ticket(BaseModel):
    ticket_id: str = Field(default="")
    employee_name: str
    employee_email: str = ""
    department: str = ""
    issue_description: str
    category: str = ""
    priority: Priority = Priority.MEDIUM
    status: TicketStatus = TicketStatus.NEW
    created_at: datetime = Field(default_factory=datetime.now)
    triage_result: dict = Field(default_factory=dict)
    knowledge_results: List[dict] = Field(default_factory=list)
    diagnosis_results: dict = Field(default_factory=dict)
    troubleshooting_steps: List[str] = Field(default_factory=list)
    resolution: dict = Field(default_factory=dict)
    escalation_info: dict = Field(default_factory=dict)
    agent_actions: List[dict] = Field(default_factory=list)
    
    def add_action(self, agent: str, action: str, result: str):
        self.agent_actions.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "result": result
        })
''')

# 6. JSON Data Files
kb_data = {
  "articles": [
    {"article_id": "KB001", "title": "Password Reset - Self Service", "category": "password_reset", "problem": "Cannot login or forgotten password", "solution": "Guide user to self-service portal", "steps": ["Go to https://passwordreset.company.com", "Enter Employee ID", "Verify OTP", "Set new password"], "tags": ["password", "login", "locked"], "success_rate": 0.95},
    {"article_id": "KB002", "title": "VPN Connection Troubleshooting", "category": "network_issue", "problem": "Unable to connect to VPN", "solution": "Restart client and verify DNS/Server", "steps": ["Check internet connection", "Restart VPN Client", "Try alternate server region", "Flush DNS cache"], "tags": ["vpn", "network", "connection"], "success_rate": 0.85},
    {"article_id": "KB003", "title": "Software Center Install", "category": "software_install", "problem": "Need software installed", "solution": "Use Company Software Center", "steps": ["Open Software Center from Start Menu", "Search requested software", "Click Install"], "tags": ["install", "software", "app"], "success_rate": 0.90},
    {"article_id": "KB004", "title": "Outlook Sync Fix", "category": "email_issue", "problem": "Emails not syncing in Outlook", "solution": "Clear cache and repair profile", "steps": ["Check internet status", "Toggle Work Offline mode", "Clear Outlook RoamCache", "Restart Outlook"], "tags": ["email", "outlook", "sync"], "success_rate": 0.88},
    {"article_id": "KB005", "title": "System Performance Optimization", "category": "performance_issue", "problem": "Computer running very slow", "solution": "Run disk cleanup and disable startup apps", "steps": ["Restart computer", "Open Task Manager to inspect memory", "Run Disk Cleanup on C: drive", "Disable unused startup apps"], "tags": ["slow", "performance", "freeze"], "success_rate": 0.80}
  ]
}
with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb_data, f, indent=2)

history_data = {
  "tickets": [
    {"ticket_id": "TK-101", "issue": "Forgot password after vacation", "category": "password_reset", "resolution": "Sent self-service reset link. Resolved.", "resolved": True, "resolution_time_hours": 0.2},
    {"ticket_id": "TK-102", "issue": "VPN drops connection constantly", "category": "network_issue", "resolution": "Flushed DNS and switched gateway region. Resolved.", "resolved": True, "resolution_time_hours": 1.0},
    {"ticket_id": "TK-103", "issue": "Phishing email with attachment", "category": "security_incident", "resolution": "Blocked sender, alerted SOC team.", "resolved": True, "resolution_time_hours": 0.5}
  ]
}
with open('data/ticket_history.json', 'w', encoding='utf-8') as f:
    json.dump(history_data, f, indent=2)

status_data = {
  "systems": [
    {"system_name": "Email Server (Exchange)", "status": "operational", "last_checked": "2025-01-01T10:00:00", "details": "Healthy"},
    {"system_name": "VPN Gateway", "status": "degraded", "last_checked": "2025-01-01T10:00:00", "details": "US-East server experiencing high latency"},
    {"system_name": "Active Directory", "status": "operational", "last_checked": "2025-01-01T10:00:00", "details": "Healthy"},
    {"system_name": "Print Server", "status": "down", "last_checked": "2025-01-01T10:00:00", "details": "Maintenance in progress"}
  ]
}
with open('data/system_status.json', 'w', encoding='utf-8') as f:
    json.dump(status_data, f, indent=2)

# 7. Tools
with open('tools/knowledge_base.py', 'w', encoding='utf-8') as f:
    f.write('''import json, os
class KnowledgeBaseTool:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
        with open(p, 'r', encoding='utf-8') as f:
            self.articles = json.load(f).get('articles', [])
    def search(self, query, category=''):
        res = []
        q = query.lower()
        for a in self.articles:
            score = 0
            if category and a.get('category','').lower() == category.lower(): score += 10
            for tag in a.get('tags', []):
                if tag.lower() in q: score += 5
            if score > 0: res.append({**a, 'relevance_score': score})
        res.sort(key=lambda x: x['relevance_score'], reverse=True)
        return res[:3]
''')

with open('tools/system_checker.py', 'w', encoding='utf-8') as f:
    f.write('''import json, os
class SystemCheckerTool:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'data', 'system_status.json')
        with open(p, 'r', encoding='utf-8') as f:
            self.systems = json.load(f).get('systems', [])
    def check_all_systems(self): return self.systems
    def get_affected_systems(self, category):
        m = {'password_reset': ['Active Directory'], 'network_issue': ['VPN Gateway'], 'email_issue': ['Email Server'], 'hardware_issue': ['Print Server']}
        names = m.get(category, [])
        return [s for s in self.systems if any(n.lower() in s['system_name'].lower() for n in names)]
    def get_problematic_systems(self): return [s for s in self.systems if s['status'] != 'operational']
''')

with open('tools/ticket_history.py', 'w', encoding='utf-8') as f:
    f.write('''import json, os
class TicketHistoryTool:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticket_history.json')
        with open(p, 'r', encoding='utf-8') as f:
            self.tickets = json.load(f).get('tickets', [])
    def search_similar_tickets(self, query, category=''):
        return [t for t in self.tickets if category and t.get('category') == category][:3]
    def get_resolution_stats(self, category):
        c = [t for t in self.tickets if t.get('category') == category]
        return {'total': len(c), 'success_rate': 0.9}
''')

with open('tools/action_executor.py', 'w', encoding='utf-8') as f:
    f.write('''class ActionExecutorTool:
    def execute(self, action_name, params=None):
        params = params or {}
        return {'success': True, 'action': action_name, 'message': f'Executed {action_name} successfully.'}
''')

with open('tools/email_notifier.py', 'w', encoding='utf-8') as f:
    f.write('''class EmailNotifierTool:
    def notify_employee(self, email, subject, body): return {'success': True, 'to': email}
    def notify_it_team(self, ticket_id, priority, summary): return {'success': True, 'ticket_id': ticket_id}
''')

# 8. Agents
with open('agents/triage_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from openai import OpenAI
from config import Config
from models.schemas import Ticket, Priority
import json

class TriageAgent:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    def analyze(self, ticket: Ticket) -> Ticket:
        print("🔍 [Triage Agent] Analyzing issue...")
        desc = ticket.issue_description.lower()
        cat = 'network_issue' if 'vpn' in desc or 'wifi' in desc or 'internet' in desc else 'password_reset' if 'password' in desc or 'login' in desc else 'security_incident' if 'phishing' in desc or 'hack' in desc else 'hardware_issue' if 'screen' in desc or 'printer' in desc else 'performance_issue'
        
        prompt = f"Classify IT issue: '{ticket.issue_description}'. Categories: password_reset, network_issue, software_install, hardware_issue, email_issue, security_incident, performance_issue, access_request. Respond JSON: {{\\"category\\": \\"...\\", \\"priority\\": \\"critical/high/medium/low\\"}}"
        try:
            resp = self.client.chat.completions.create(model=Config.MODEL_NAME, messages=[{'role': 'user', 'content': prompt}], temperature=0.1, response_format={'type': 'json_object'})
            data = json.loads(resp.choices[0].message.content)
            cat = data.get('category', cat)
            ticket.priority = Priority(data.get('priority', 'medium'))
        except:
            ticket.priority = Priority.HIGH if cat == 'security_incident' else Priority.MEDIUM

        ticket.category = cat
        ticket.triage_result = {'category': cat, 'priority': ticket.priority.value, 'auto_resolvable': cat in ['password_reset', 'software_install']}
        ticket.status = 'triaged'
        ticket.add_action('triage_agent', 'classify', f'Category: {cat}, Priority: {ticket.priority.value}')
        print(f"   ✅ Classified as {cat} [{ticket.priority.value}]")
        return ticket
''')

with open('agents/knowledge_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from tools.knowledge_base import KnowledgeBaseTool
from tools.ticket_history import TicketHistoryTool
from models.schemas import Ticket

class KnowledgeAgent:
    def __init__(self):
        self.kb = KnowledgeBaseTool()
        self.history = TicketHistoryTool()
    def investigate(self, ticket: Ticket) -> Ticket:
        print("📚 [Knowledge Agent] Searching knowledge base...")
        ticket.knowledge_results = self.kb.search(ticket.issue_description, ticket.category)
        ticket.add_action('knowledge_agent', 'search', f"Found {len(ticket.knowledge_results)} KB articles")
        return ticket
''')

with open('agents/diagnosis_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from tools.system_checker import SystemCheckerTool
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
''')

with open('agents/troubleshoot_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from models.schemas import Ticket

class TroubleshootAgent:
    def troubleshoot(self, ticket: Ticket) -> Ticket:
        print("🛠️ [Troubleshoot Agent] Generating steps...")
        steps = ['Step 1: Check hardware and basic network connections.', 'Step 2: Clear application cache and restart.', 'Step 3: Run diagnostic tests.']
        if ticket.knowledge_results:
            steps = ticket.knowledge_results[0].get('steps', steps)
        ticket.troubleshooting_steps = steps
        ticket.add_action('troubleshoot_agent', 'generate_steps', f"{len(steps)} steps generated")
        return ticket
''')

with open('agents/resolution_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from tools.action_executor import ActionExecutorTool
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
''')

with open('agents/escalation_agent.py', 'w', encoding='utf-8') as f:
    f.write('''from tools.email_notifier import EmailNotifierTool
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
''')

with open('agents/orchestrator.py', 'w', encoding='utf-8') as f:
    f.write('''from models.schemas import Ticket, Priority
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
        print(f"\\n{'='*55}\\n🎫 TICKET {ticket.ticket_id}: {employee_name}\\n📝 Issue: {issue_description}\\n{'='*55}")
        
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
                
        print(f"\\n📊 FINAL STATUS: {ticket.status.upper()}")
        for a in ticket.agent_actions:
            print(f"   ➔ [{a['agent']}]: {a['result']}")
        print(f"{'='*55}")
        return ticket
''')

# 9. main.py
with open('main.py', 'w', encoding='utf-8') as f:
    f.write('''from agents.orchestrator import Orchestrator
import sys

def run_demo():
    print("🤖 STARTING AGENTIC IT HELPDESK DEMO...\\n")
    orchestrator = Orchestrator()
    scenarios = [
        ("Amit Sharma", "I forgot my password and my account is locked."),
        ("Priya Patel", "VPN is disconnecting constantly and giving timeout error."),
        ("Vikram Singh", "Received suspicious phishing email with an attachment."),
        ("Sneha Roy", "My laptop monitor screen has lines and is flickering.")
    ]
    for name, issue in scenarios:
        orchestrator.process_ticket(name, issue)

if __name__ == '__main__':
    run_demo()
''')

print("🎉 ALL FILES AND DIRECTORIES CREATED SUCCESSFULLY!")