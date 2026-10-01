from agents.orchestrator import Orchestrator
import sys

def run_demo():
    print("🤖 STARTING AGENTIC IT HELPDESK DEMO...\n")
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
