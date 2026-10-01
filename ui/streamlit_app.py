import streamlit as st
import sys
import os

# Root folder add karo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator import Orchestrator

st.set_page_config(page_title="AI IT Service Desk", page_icon="🤖", layout="wide")

# Header
st.title("🤖 AI IT Service Desk - Autonomous Resolution Agent")
st.caption("Agentic AI System: Ticket Triage ➔ Knowledge Base ➔ System Diagnosis ➔ Troubleshooting ➔ Resolution ➔ Escalation")

@st.cache_resource
def get_orchestrator():
    return Orchestrator()

orchestrator = get_orchestrator()

# Two columns layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Submit IT Issue")
    name = st.text_input("Employee Name", value="Amit Sharma")
    email = st.text_input("Employee Email", value="amit.sharma@company.com")
    dept = st.selectbox("Department", ["IT", "Sales", "Engineering", "HR", "Finance", "Marketing"])
    
    # Pre-set issue buttons
    st.markdown("**Quick Test Issues:**")
    q1, q2 = st.columns(2)
    default_text = ""
    if q1.button("🔑 Password Lock"):
        default_text = "I forgot my password and my account is locked."
    if q2.button("🌐 VPN Disconnect"):
        default_text = "VPN is disconnecting constantly and giving timeout error."
    if q1.button("⚠️ Phishing Email"):
        default_text = "Received suspicious phishing email with an attachment."
    if q2.button("🖥️ Screen Flickering"):
        default_text = "My laptop monitor screen has lines and is flickering."
        
    issue = st.text_area("Describe your IT issue", value=default_text, height=120)
    submit = st.button("🚀 Process with AI Agents", use_container_width=True)

with col2:
    st.subheader("📊 Agent Execution Pipeline")
    if submit and issue:
        with st.spinner("Agents investigating issue in real-time..."):
            ticket = orchestrator.process_ticket(name, issue, email, dept)
            
            # Status Badge
            if ticket.status == "resolved":
                st.success(f"✅ Status: RESOLVED ({ticket.category.upper()})")
            else:
                st.error(f"🚨 Status: ESCALATED ({ticket.category.upper()})")
                
            st.markdown(f"**Ticket ID:** `{ticket.ticket_id}` | **Priority:** `{ticket.priority.value.upper()}`")
            st.markdown("---")
            
            st.markdown("### 📜 Autonomous Agent Actions:")
            agent_icons = {
                "triage_agent": "🔍",
                "knowledge_agent": "📚",
                "diagnosis_agent": "🔧",
                "troubleshoot_agent": "🛠️",
                "resolution_agent": "✨",
                "escalation_agent": "🚨"
            }
            for action in ticket.agent_actions:
                icon = agent_icons.get(action['agent'], "⚙️")
                with st.expander(f"{icon} {action['agent'].replace('_', ' ').title()}", expanded=True):
                    st.write(action['result'])
                    st.caption(f"Timestamp: {action['timestamp']}")
                    
            if ticket.troubleshooting_steps:
                st.markdown("### 🛠️ Troubleshooting Plan:")
                for i, step in enumerate(ticket.troubleshooting_steps, 1):
                    st.write(f"**{i}.** {step}")
                    
            if ticket.escalation_info:
                st.warning(f"**Escalated To:** {ticket.escalation_info.get('escalate_to')}  \n**Reason:** {ticket.escalation_info.get('reason')}")
    elif submit:
        st.error("Please describe your issue first!")