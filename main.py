"""
Entry point for Streamlit application
Run with: streamlit run main.py
"""

# Import and run the app directly
from src.ui.app import (
    render_header,
    render_sidebar,
    render_analysis_tab,
    render_history_tab,
    get_llm_client,
    get_transcriber,
)
import streamlit as st

# Render the application
render_header()
weights = render_sidebar()

# Main tabs
tab1, tab2 = st.tabs(["📝 Analysis", "📜 History"])

with tab1:
    render_analysis_tab(weights)

with tab2:
    render_history_tab()
