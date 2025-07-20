"""
Main Streamlit application for College Basketball Opponent Scouting Dashboard.
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="College Basketball Scouting Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the backend API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def main():
    """Main application function."""
    st.title("🏀 College Basketball Opponent Scouting Dashboard")
    st.markdown("---")
    
    # Check API status
    api_status = check_api_health()
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Select Page",
            ["Dashboard", "Team Analysis", "Player Stats", "Game Preparation", "Data Sources"]
        )
        
        st.markdown("---")
        st.subheader("API Status")
        if api_status:
            st.success("✅ Backend API Connected")
        else:
            st.error("❌ Backend API Disconnected")
            st.warning("Make sure the FastAPI backend is running on port 8000")
    
    # Main content area
    if page == "Dashboard":
        show_dashboard()
    elif page == "Team Analysis":
        show_team_analysis()
    elif page == "Player Stats":
        show_player_stats()
    elif page == "Game Preparation":
        show_game_preparation()
    elif page == "Data Sources":
        show_data_sources()

def show_dashboard():
    """Display the main dashboard."""
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Teams Analyzed", "0", "0")
    
    with col2:
        st.metric("Games Scouted", "0", "0")
    
    with col3:
        st.metric("Reports Generated", "0", "0")
    
    with col4:
        st.metric("Last Updated", "Never", "")
    
    st.markdown("---")
    
    # Placeholder for charts and data
    st.subheader("Recent Activity")
    st.info("No data available yet. Start by configuring data sources and analyzing teams.")

def show_team_analysis():
    """Display team analysis page."""
    st.header("Team Analysis")
    
    team_name = st.text_input("Enter team name to analyze:")
    
    if team_name:
        st.subheader(f"Analysis for {team_name}")
        st.info("Team analysis functionality will be implemented when connected to data sources.")
    else:
        st.info("Enter a team name to begin analysis.")

def show_player_stats():
    """Display player statistics page."""
    st.header("Player Statistics")
    st.info("Player statistics functionality will be implemented when connected to data sources.")

def show_game_preparation():
    """Display game preparation page."""
    st.header("Game Preparation")
    st.info("Game preparation tools will be available when the backend is fully configured.")

def show_data_sources():
    """Display data sources configuration."""
    st.header("Data Sources")
    
    st.subheader("Available Sources")
    
    # BartTorvik
    with st.expander("BartTorvik (T-Rank)", expanded=True):
        st.write("**Status**: Not configured")
        st.write("**Description**: Primary source for team rankings and statistics")
        st.write("**Access**: Free CSV/JSON downloads")
    
    # KenPom
    with st.expander("KenPom"):
        st.write("**Status**: Not configured")
        st.write("**Description**: Advanced basketball analytics")
        st.write("**Access**: Subscription required")
    
    # Sports Reference
    with st.expander("Sports Reference"):
        st.write("**Status**: Not configured")
        st.write("**Description**: Backup source for additional metrics")
        st.write("**Access**: Web scraping")
    
    st.markdown("---")
    st.subheader("Configuration")
    st.info("Data source configuration will be handled through the backend API and environment variables.")

if __name__ == "__main__":
    main()