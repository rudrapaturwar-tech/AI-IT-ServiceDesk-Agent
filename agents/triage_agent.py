from openai import OpenAI
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
        
        prompt = f"Classify IT issue: '{ticket.issue_description}'. Categories: password_reset, network_issue, software_install, hardware_issue, email_issue, security_incident, performance_issue, access_request. Respond JSON: {{\"category\": \"...\", \"priority\": \"critical/high/medium/low\"}}"
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
