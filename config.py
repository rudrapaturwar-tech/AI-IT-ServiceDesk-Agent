import os
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
