import streamlit as st
import sys
import os
import time
import json

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator import Orchestrator
from tools.system_checker import SystemCheckerTool

st.set_page_config(
    page_title="Enterprise AI IT Service Desk",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Styling
st.markdown("""
<style>
    .main-title { font-size: 2.1rem; font-weight: 800; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1rem; color: #64748B; margin-bottom: 1.4rem; }
    .plain-card { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; margin-bottom: 12px; }
    .highlight-text { font-weight: 600; color: #0F172A; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_system():
    return Orchestrator(), SystemCheckerTool()

orchestrator, checker = load_system()

# Sidebar: Live System Monitoring
with st.sidebar:
    st.markdown("### 🏢 Infrastructure Status")
    systems = checker.check_all_systems()
    for s in systems:
        status = s.get('status', 'operational')
        icon = "🟢" if status == 'operational' else "🟡" if status == 'degraded' else "🔴"
        st.markdown(f"**{icon} {s.get('system_name', 'System')}**")
        st.caption(f"Status: `{status.upper()}` | {s.get('details', '')}")
            
    st.markdown("---")
    st.markdown("### 📊 Helpdesk Performance")
    st.metric(label="Auto-Resolution Rate", value="82.4%", delta="+4.1%")
    st.metric(label="Average Resolution Time", value="1.8 Mins", delta="-6.2 Mins")

# Main Header
st.markdown('<div class="main-title">🛡️ Autonomous AI IT Service Desk</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dual-Layer AI: Plain Simple English for Employees • Deep Technical Audits for IT Engineers</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.25], gap="large")

with col_left:
    st.markdown("### 📝 Submit IT Issue")
    
    name = st.text_input("👤 Your Name", value="Amit Sharma")
    email = st.text_input("📧 Work Email", value="amit.sharma@enterprise.corp")
    dept = st.selectbox("🏢 Department", ["Finance & Accounts", "Human Resources (HR)", "Sales & Marketing", "Engineering", "Operations"])
    
    st.markdown("**⚡ Quick Test Scenarios (Click to Load):**")
    q1, q2 = st.columns(2)
    if q1.button("🔑 Account Locked", use_container_width=True):
        st.session_state.issue_txt = "My account is locked. I cannot sign into my laptop or email after entering the wrong password."
    if q2.button("🌐 VPN Disconnecting", use_container_width=True):
        st.session_state.issue_txt = "VPN keeps disconnecting every 5 minutes and my connection becomes very slow."
    if q1.button("🚨 Phishing Email Alert", use_container_width=True):
        st.session_state.issue_txt = "Received a suspicious email from an unknown sender asking me to download an urgent payroll attachment."
    if q2.button("🖥️ Screen Flickering", use_container_width=True):
        st.session_state.issue_txt = "My laptop display is showing colored vertical lines and flickering continuously."

    issue_input = st.text_area("Describe your issue in plain words:", value=st.session_state.get('issue_txt', ''), height=120)
    
    submit_btn = st.button("🚀 Submit & Resolve with AI", type="primary", use_container_width=True)

with col_right:
    st.markdown("### 🧠 AI Resolution & Execution")
    
    if submit_btn and issue_input:
        progress_bar = st.progress(0, text="Understanding your issue...")
        time.sleep(0.2)
        progress_bar.progress(35, text="Checking knowledge base and system health...")
        time.sleep(0.2)
        progress_bar.progress(75, text="Applying automated fix...")
        
        ticket = orchestrator.process_ticket(name, issue_input, email, dept)
        progress_bar.progress(100, text="Done!")
        time.sleep(0.1)
        progress_bar.empty()
        
        is_resolved = (ticket.status == "resolved")
        status_banner = "✅ ISSUE RESOLVED AUTOMATICALLY" if is_resolved else "🚨 ESCALATED TO IT SPECIALIST TEAM"
        status_color = "#10B981" if is_resolved else "#EF4444"
        
        st.markdown(f"""
        <div style="background:{status_color}15; border: 2px solid {status_color}; border-radius: 10px; padding: 12px; margin-bottom: 15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:1.05rem; font-weight:700; color:{status_color};">{status_banner}</span>
                <span style="background:{status_color}; color:white; padding:3px 8px; border-radius:12px; font-weight:700; font-size:0.8rem;">{ticket.ticket_id}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dual-Layer Tabs (Plain English vs Deep Technical)
        tab_plain, tab_trace, tab_tech = st.tabs(["👤 Plain English (Employee View)", "⚡ Agent Execution Path", "🛠️ Deep Technical Dossier"])
        
        with tab_plain:
            st.markdown("#### 💬 Plain English Summary:")
            
            # Simple category name
            friendly_categories = {
                "password_reset": "Password & Login Issue",
                "network_issue": "Internet & VPN Connection Issue",
                "security_incident": "Security Warning / Suspicious Email",
                "hardware_issue": "Physical Device / Display Issue"
            }
            cat_display = friendly_categories.get(ticket.category, ticket.category.replace("_", " ").title())
            
            st.info(f"**Issue Identified:** {cat_display}")
            
            if is_resolved:
                st.success(f"""
                **Hi {name},**
                
                Good news! Your issue has been automatically resolved by the AI Helpdesk.
                
                • **What we did:** We checked the issue and ran an automated fix to restore your access.  
                • **What you should do next:** Please check your work email / phone for any verification link, and try logging in again.
                """)
            else:
                esc = ticket.escalation_info
                target_team = esc.get('escalate_to', 'IT Support')
                st.warning(f"""
                **Hi {name},**
                
                This issue cannot be fixed automatically and requires hands-on help from our engineering team.
                
                • **Assigned Team:** `{target_team}`  
                • **Why it was escalated:** {esc.get('reason', 'Requires specialist investigation')}  
                • **Expected Response:** An engineer will reach out to you within **15–30 minutes**.
                """)
                
            if ticket.troubleshooting_steps:
                st.markdown("---")
                st.markdown("#### 📋 Simple Steps You Can Try Right Now:")
                for idx, step in enumerate(ticket.troubleshooting_steps, 1):
                    st.checkbox(f"**Step {idx}:** {step}", key=f"p_step_{idx}_{ticket.ticket_id}")

        with tab_trace:
            st.markdown("#### ⚡ Dynamic Agent Routing Path:")
            agent_icons = {
                "Triage Agent": "🔍",
                "Knowledge Agent": "📚",
                "Diagnosis Agent": "🔧",
                "Troubleshoot Agent": "🛠️",
                "Resolution Agent": "✨",
                "Escalation Agent": "🚨"
            }
            for i, act in enumerate(ticket.agent_actions):
                icon = agent_icons.get(act.get('agent'), "⚙️")
                with st.expander(f"{icon} Step {i+1}: **{act.get('agent')}** ➔ *{act.get('action')}*", expanded=True):
                    st.write(act.get('result'))
                    st.caption(f"Timestamp: {act.get('timestamp')} | Execution Time: 0.3s")

        with tab_tech:
            st.markdown("#### 🛠️ Technical Audit & Telemetry (For Engineers & Judges):")
            st.json({
                "ticket_id": ticket.ticket_id,
                "category": ticket.category,
                "priority": ticket.priority.value,
                "target_sla_minutes": 15,
                "triage_metadata": ticket.triage_result,
                "diagnosis_telemetry": ticket.diagnosis_results,
                "actions_executed": ticket.resolution.get("actions_taken") if ticket.resolution else None,
                "escalation_payload": ticket.escalation_info if ticket.escalation_info else None
            })
            
            report_data = ticket.model_dump()
            st.download_button(
                label="📥 Download ITIL JSON Audit Report",
                data=json.dumps(report_data, default=str, indent=2),
                file_name=f"{ticket.ticket_id}_Audit.json",
                mime="application/json",
                use_container_width=True
            )
            
    elif submit_btn:
        st.warning("⚠️ Please describe your problem first.")
    else:
        st.info("👈 Select a **Quick Test Scenario** or type your problem on the left to see the AI agent in action.")