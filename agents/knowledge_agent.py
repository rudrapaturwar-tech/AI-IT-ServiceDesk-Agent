from tools.knowledge_base import KnowledgeBaseTool
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
