from pydantic import BaseModel, Field
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
