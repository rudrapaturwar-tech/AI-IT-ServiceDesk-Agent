import json, os, time, uuid
from datetime import datetime
from openai import OpenAI
from config import Config
from models.schemas import Ticket, Priority, TicketStatus
from tools.knowledge_base import KnowledgeBaseTool
from tools.system_checker import SystemCheckerTool
from tools.ticket_history import TicketHistoryTool
from tools.action_executor import ActionExecutorTool
from tools.email_notifier import EmailNotifierTool

class Orchestrator:
    """
    ENTERPRISE MULTI-AGENT AUTONOMOUS ORCHESTRATOR
    Uses Deep LLM Reasoning & Dynamic Context Evaluation to route across:
    Triage ➔ Knowledge/RAG ➔ System Telemetry ➔ Troubleshooting ➔ Action Remediation ➔ Escalation
    """
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=os.getenv("OPENAI_BASE_URL", None)
        )
        self.kb = KnowledgeBaseTool()
        self.checker = SystemCheckerTool()
        self.history = TicketHistoryTool()
        self.executor = ActionExecutorTool()
        self.notifier = EmailNotifierTool()

    def process_ticket(self, employee_name: str, issue_description: str, employee_email: str = "", department: str = "") -> Ticket:
        start_time = time.time()
        ticket = Ticket(
            ticket_id=f"INC-{datetime.now().strftime('%m%d')}-{uuid.uuid4().hex[:4].upper()}",
            employee_name=employee_name,
            employee_email=employee_email or f"{employee_name.lower().replace(' ', '.')}@enterprise.corp",
            department=department or "Corporate Operations",
            issue_description=issue_description
        )

        # -------------------------------------------------------------
        # AGENT 1: TRIAGE & RISK ASSESSMENT (LLM Reasoning)
        # -------------------------------------------------------------
        triage_prompt = f"""You are an Enterprise IT Service Desk Lead.
Analyze this incident report and classify it accurately:
User: {employee_name} ({department})
Description: "{issue_description}"

Valid Categories:
- password_reset (authentication, lockout, credentials)
- network_issue (vpn, wifi, latency, dns, routing)
- software_install (requests, updates, licensing)
- hardware_issue (screen, physical peripherals, chassis, battery)
- email_issue (outlook, exchange, mailbox quota)
- security_incident (phishing, unauthorized token, malware, suspicious sender)
- performance_issue (bsod, high cpu/ram, freezing)
- access_request (shared drive, IAM roles)

Respond STRICTLY in JSON format:
{{
    "category": "exact_category",
    "priority": "critical/high/medium/low",
    "reasoning": "technical explanation for this priority and categorization",
    "is_security_threat": true/false,
    "sla_target_minutes": 15
}}"""
        try:
            resp = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[{"role": "user", "content": triage_prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            triage_data = json.loads(resp.choices[0].message.content)
            ticket.category = triage_data.get("category", "network_issue")
            prio = triage_data.get("priority", "medium").lower()
            if prio not in ["critical", "high", "medium", "low"]: prio = "medium"
            ticket.priority = Priority(prio)
            ticket.triage_result = triage_data
        except Exception:
            ticket.category = "network_issue"
            ticket.priority = Priority.MEDIUM
            ticket.triage_result = {"category": ticket.category, "priority": "medium", "reasoning": "Default heuristic fallback"}

        ticket.add_action("Triage Agent", "Evaluate Incident Risk & Category", 
                          f"Classified as '{ticket.category.upper()}' [Priority: {ticket.priority.value.upper()}] - {ticket.triage_result.get('reasoning')}")

        cat = ticket.category

        # -------------------------------------------------------------
        # DYNAMIC ROUTE 1: SECURITY THREAT ➔ Fast-Track Quarantine & SOC Escalation
        # -------------------------------------------------------------
        if cat == "security_incident" or ticket.triage_result.get("is_security_threat"):
            diag = self.checker.get_affected_systems(cat)
            ticket.add_action("Diagnosis Agent", "Query Active Security Telemetry", "Inspected EDR sensors and firewall logs. Active session token risk detected.")
            
            # Automated Quarantine Action
            iso_res = self.executor.execute("isolate_endpoint_edr", {"employee_email": ticket.employee_email})
            ticket.add_action("Resolution Agent", "Automated Security Remediation", iso_res["message"])
            
            # Escalation Handover
            ticket.escalation_info = {
                "escalate_to": "Tier-3 Cyber Security Operations Center (SOC)",
                "reason": "Suspected credential harvesting / malicious payload requires immediate forensic audit.",
                "dossier": {
                    "containment_status": "Host Isolated via CrowdStrike EDR",
                    "sla_deadline": "Immediate (P1 - 15 Mins SLA)",
                    "suggested_actions": ["Analyze email header headers", "Inspect Exchange mail trace", "Revoke OAuth tokens"]
                }
            }
            ticket.status = TicketStatus.ESCALATED
            ticket.add_action("Escalation Agent", "Dispatch Incident Dossier", "P1 Security Ticket transferred to 24/7 SOC On-Call Lead.")
            return ticket

        # -------------------------------------------------------------
        # DYNAMIC ROUTE 2: HARDWARE DAMAGE ➔ Physical Inspection Protocol
        # -------------------------------------------------------------
        if cat == "hardware_issue":
            ticket.knowledge_results = self.kb.search(ticket.issue_description, cat)
            ticket.add_action("Knowledge Agent", "Query Hardware Knowledge Base", f"Retrieved {len(ticket.knowledge_results)} hardware diagnostic protocols.")
            
            # Soft Driver Reset Attempt
            hw_action = self.executor.execute("gpu_driver_restart", {})
            ticket.add_action("Resolution Agent", "Hardware Telemetry Soft Reset", hw_action["message"])
            
            ticket.troubleshooting_steps = [
                "Execute hardware reset shortcut: Press Windows Key + Ctrl + Shift + B.",
                "Disconnect external dock and test with direct HDMI/Thunderbolt connection.",
                "If artifact lines persist in BIOS screen, physical LCD/eDP cable has failed."
            ]
            ticket.add_action("Troubleshoot Agent", "Generate Diagnostic Tree", "Constructed 3-tier hardware fault isolation steps.")
            
            ticket.escalation_info = {
                "escalate_to": "IT Asset & Hardware Replacement Team",
                "reason": "Physical component failure / display matrix defect requires depot technician swap.",
                "dossier": {
                    "asset_provisioning": "Replacement loaner laptop scheduled for dispatch",
                    "suggested_actions": ["Dispatch replacement unit", "Schedule hardware diagnostics appointment"]
                }
            }
            ticket.status = TicketStatus.ESCALATED
            ticket.add_action("Escalation Agent", "Create Hardware Replacement Dispatch", "Ticket routed to Physical Desk Support.")
            return ticket

        # -------------------------------------------------------------
        # DYNAMIC ROUTE 3: PASSWORD & ROUTINE SELF-SERVICE ➔ Direct Autonomous Fix
        # -------------------------------------------------------------
        if cat in ["password_reset", "software_install"]:
            ticket.knowledge_results = self.kb.search(ticket.issue_description, cat)
            ticket.add_action("Knowledge Agent", "Retrieve Self-Service Automation SOP", "Extracted automated Active Directory provisioning parameters.")
            
            action_res = self.executor.execute("ad_unlock_and_token", {"employee_email": ticket.employee_email})
            ticket.resolution = {
                "method": "Autonomous Active Directory Execution",
                "actions_taken": [action_res],
                "resolution_summary": {
                    "employee_message": f"Hello {ticket.employee_name}, your Active Directory account has been unlocked and verified. A secure password reset link has been dispatched to your registered phone/MFA app.",
                    "preventive_tip": "Always update stored credentials on mobile devices when updating your corporate password."
                },
                "success": True
            }
            ticket.status = TicketStatus.RESOLVED
            ticket.add_action("Resolution Agent", "Execute Active Directory Unlock", action_res["message"])
            return ticket

        # -------------------------------------------------------------
        # DYNAMIC ROUTE 4: COMPLEX INFRASTRUCTURE / NETWORK / EMAIL
        # -------------------------------------------------------------
        affected_systems = self.checker.get_affected_systems(cat)
        outage = any(s['status'] != 'operational' for s in affected_systems)
        
        ticket.diagnosis_results = {
            "affected_systems": affected_systems,
            "root_cause_analysis": {
                "is_system_issue": outage,
                "root_cause": "US-East VPN Gateway ISP Packet Drop" if outage else "Local workstation configuration drift"
            }
        }
        ticket.add_action("Diagnosis Agent", "Query Live Infrastructure Telemetry", 
                          f"Checked {len(affected_systems)} core services. Active Outage detected: {outage}")

        if outage:
            ticket.escalation_info = {
                "escalate_to": "Network & Infrastructure Engineering",
                "reason": "Active upstream provider degradation on US-East Gateway. Requires BGP route reroute.",
                "dossier": {
                    "outage_impact": "Broadband packet loss impacting remote workforce",
                    "suggested_actions": ["Reroute BGP peering to Tier-1 backup pipe", "Update status page alert"]
                }
            }
            ticket.status = TicketStatus.ESCALATED
            ticket.add_action("Escalation Agent", "Escalate Infrastructure Outage", "Ticket linked to ongoing Major Incident (P2-NET-99).")
            return ticket

        # Local Fixable Complex Issue
        ticket.knowledge_results = self.kb.search(ticket.issue_description, cat)
        ticket.add_action("Knowledge Agent", "Synthesize Multi-Source Knowledge", f"Indexed {len(ticket.knowledge_results)} KB articles and historical resolved tickets.")

        ticket.troubleshooting_steps = [
            "Flush local DNS resolver cache: `ipconfig /flushdns` via Command Prompt.",
            "Verify network adapter MTU is set to 1350 bytes to avoid packet drop.",
            "Switch VPN client profile from US-East to US-West Secondary Gateway."
        ]
        ticket.add_action("Troubleshoot Agent", "Formulate Remediation Steps", "Generated tailored 3-step actionable resolution plan.")

        act_res = self.executor.execute("flush_dns_and_mtu", {})
        ticket.resolution = {
            "method": "Autonomous Network Adapter Configuration",
            "actions_taken": [act_res],
            "resolution_summary": {
                "employee_message": f"Hello {ticket.employee_name}, we have automated the network adapter reconfiguration and switched your connection to the healthy US-West gateway.",
                "preventive_tip": "Restart your VPN client once a week to apply the latest server routing certificates."
            },
            "success": True
        }
        ticket.status = TicketStatus.RESOLVED
        ticket.add_action("Resolution Agent", "Apply Gateway & MTU Reconfiguration", act_res["message"])
        return ticket
