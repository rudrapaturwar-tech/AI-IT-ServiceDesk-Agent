from models.schemas import Ticket

class TroubleshootAgent:
    def troubleshoot(self, ticket: Ticket) -> Ticket:
        print("🛠️ [Troubleshoot Agent] Generating steps...")
        steps = ['Step 1: Check hardware and basic network connections.', 'Step 2: Clear application cache and restart.', 'Step 3: Run diagnostic tests.']
        if ticket.knowledge_results:
            steps = ticket.knowledge_results[0].get('steps', steps)
        ticket.troubleshooting_steps = steps
        ticket.add_action('troubleshoot_agent', 'generate_steps', f"{len(steps)} steps generated")
        return ticket
