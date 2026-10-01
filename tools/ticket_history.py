import json, os
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
