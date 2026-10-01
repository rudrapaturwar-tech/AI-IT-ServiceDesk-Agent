import json, os
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
