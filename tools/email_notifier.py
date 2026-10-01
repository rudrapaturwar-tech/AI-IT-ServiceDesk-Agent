class EmailNotifierTool:
    def notify_employee(self, email, subject, body): return {'success': True, 'to': email}
    def notify_it_team(self, ticket_id, priority, summary): return {'success': True, 'ticket_id': ticket_id}
