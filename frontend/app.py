import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import non-Streamlit modules first
import httpx
import asyncio
from datetime import datetime

# Import Streamlit
import streamlit as st

# Must be first streamlit command
st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NOW import page modules (after set_page_config)
import frontend.pages.job_input as job_input
import frontend.pages.resume_upload as resume_upload
import frontend.pages.match_display as match_display
import frontend.pages.letter_display as letter_display
import frontend.pages.history as history

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "job_input"
if "job_data" not in st.session_state:
    st.session_state.job_data = None
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "match_data" not in st.session_state:
    st.session_state.match_data = None
if "letter_data" not in st.session_state:
    st.session_state.letter_data = None


# Sidebar navigation
with st.sidebar:
    st.title("💼 Job Assistant")
    st.markdown("---")
    
    if st.button("📝 New Job", use_container_width=True):
        st.session_state.page = "job_input"
        st.rerun()
    
    if st.button("📄 Upload Resume", use_container_width=True, 
                 disabled=not st.session_state.job_data):
        st.session_state.page = "resume_upload"
        st.rerun()
    
    if st.button("🎯 View Match", use_container_width=True,
                 disabled=not st.session_state.resume_data):
        st.session_state.page = "match_display"
        st.rerun()
    
    if st.button("✉️ Generate Letter", use_container_width=True,
                 disabled=not st.session_state.match_data):
        st.session_state.page = "letter_display"
        st.rerun()
    
    if st.button("📚 History", use_container_width=True):
        st.session_state.page = "history"
        st.rerun()
    
    st.markdown("---")
    st.caption("Complete ML Job Application Assistant")


# Page routing
if st.session_state.page == "job_input":
    job_input.show()
elif st.session_state.page == "resume_upload":
    resume_upload.show()
elif st.session_state.page == "match_display":
    match_display.show()
elif st.session_state.page == "letter_display":
    letter_display.show()
elif st.session_state.page == "history":
    history.show()