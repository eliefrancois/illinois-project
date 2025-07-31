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
import os

# Get API URL from environment variable or use default
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

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
    
    # Fetch data from backend
    try:
        # Get all teams
        response = requests.get(f"{API_BASE_URL}/teams/list")
        if response.status_code == 200:
            teams_data = response.json()
            total_teams = len(teams_data.get("teams", []))
        else:
            total_teams = 0
            
        # Get some sample team data for recent activity
        response = requests.get(f"{API_BASE_URL}/teams/search?query=Illinois")
        if response.status_code == 200:
            recent_teams = response.json().get("teams", [])
        else:
            recent_teams = []
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        total_teams = 0
        recent_teams = []
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Teams Available", total_teams, f"+{total_teams}")
    
    with col2:
        st.metric("Data Sources", "1", "+1")  # BartTorvik
    
    with col3:
        st.metric("API Status", "Connected", "✅")
    
    with col4:
        from datetime import datetime
        st.metric("Last Updated", datetime.now().strftime("%H:%M"), "Live")
    
    st.markdown("---")
    
    # Show recent activity
    st.subheader("Recent Activity")
    
    if recent_teams:
        st.success(f"✅ Successfully connected to BartTorvik data source")
        st.write(f"**Found {len(recent_teams)} teams matching 'Illinois':**")
        
        # Display recent teams
        for team in recent_teams[:5]:  # Show first 5
            st.write(f"• **{team['team']}** ({team['conference']}) - {team['record']} record")
    else:
        st.info("No recent activity. Try searching for a team in the Team Analysis section.")

def show_team_analysis():
    """Display team analysis page."""
    st.header("Team Analysis")
    
    # Search for teams
    search_query = st.text_input("Search for a team:", placeholder="e.g., Illinois, Duke, Houston")
    
    if search_query:
        try:
            response = requests.get(f"{API_BASE_URL}/teams/search?query={search_query}")
            if response.status_code == 200:
                teams = response.json().get("teams", [])
                
                if teams:
                    st.success(f"Found {len(teams)} teams matching '{search_query}'")
                    
                    # Let user select a team
                    team_options = [f"{team['team']} ({team['conference']})" for team in teams]
                    selected_team_display = st.selectbox("Select a team to analyze:", team_options)
                    
                    if selected_team_display:
                        # Extract team name from display string
                        selected_team = selected_team_display.split(" (")[0]
                        
                        # Get detailed team data
                        team_response = requests.get(f"{API_BASE_URL}/teams/{selected_team}")
                        if team_response.status_code == 200:
                            team_data = team_response.json().get("team", {})
                            
                            st.subheader(f"📊 {selected_team} Analysis")
                            
                            # Display team stats
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Rank", team_data.get("rank", "N/A"))
                                st.metric("Conference", team_data.get("conf", "N/A"))
                            
                            with col2:
                                st.metric("Record", team_data.get("record", "N/A"))
                                st.metric("Wins", team_data.get("wins", "N/A"))
                            
                            with col3:
                                st.metric("Barthag Rating", f"{team_data.get('barthag', 0):.3f}")
                                st.metric("AdjOE", f"{team_data.get('adjoe', 0):.1f}")
                            
                            with col4:
                                st.metric("AdjDE", f"{team_data.get('adjde', 0):.1f}")
                                st.metric("WAB", f"{team_data.get('WAB', 0):.1f}")
                            
                            st.markdown("---")
                            
                            # Team comparison
                            st.subheader("🔍 Compare with Another Team")
                            compare_team = st.text_input("Enter team to compare with:", placeholder="e.g., Duke")
                            
                            if compare_team:
                                compare_response = requests.get(f"{API_BASE_URL}/teams/compare/{selected_team}/{compare_team}")
                                if compare_response.status_code == 200:
                                    comparison = compare_response.json().get("comparison", {})
                                    
                                    if comparison:
                                        st.success(f"Comparison: {selected_team} vs {compare_team}")
                                        
                                        # Show comparison metrics
                                        comp_data = comparison.get("comparison", {})
                                        if comp_data:
                                            st.write("**Key Metrics Comparison:**")
                                            for metric, data in comp_data.items():
                                                if isinstance(data, dict):
                                                    st.write(f"• **{metric.upper()}**: {selected_team} ({data.get('team1_value', 0):.3f}) vs {compare_team} ({data.get('team2_value', 0):.3f})")
                                                    advantage = data.get('advantage', '')
                                                    if advantage == 'team1':
                                                        st.write(f"  → **{selected_team}** has the advantage")
                                                    elif advantage == 'team2':
                                                        st.write(f"  → **{compare_team}** has the advantage")
                                else:
                                    st.error(f"Could not compare with {compare_team}")
                        else:
                            st.error(f"Could not fetch data for {selected_team}")
                else:
                    st.warning(f"No teams found matching '{search_query}'")
            else:
                st.error("Error searching for teams")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Enter a team name to search and analyze.")

def show_player_stats():
    """Display player statistics page."""
    st.header("Player Statistics & Roster Analysis")
    
    st.markdown("---")
    
    # Team Selection for Roster Analysis
    st.subheader("🔍 Select Team for Roster Analysis")
    
    # Get all teams for selection
    try:
        response = requests.get(f"{API_BASE_URL}/teams/list")
        if response.status_code == 200:
            all_teams = response.json().get("teams", [])
            
            # Create a search box for teams
            team_search = st.text_input("Search for a team:", placeholder="e.g., Illinois, Duke, Houston")
            
            if team_search:
                # Filter teams based on search
                filtered_teams = [team for team in all_teams if team_search.lower() in team.lower()]
                
                if filtered_teams:
                    selected_team = st.selectbox("Select team:", filtered_teams[:20])  # Limit to first 20
                    
                    if selected_team:
                        # Get team data
                        team_response = requests.get(f"{API_BASE_URL}/teams/{selected_team}")
                        if team_response.status_code == 200:
                            team_data = team_response.json().get("team", {})
                            
                            st.success(f"📊 Analyzing {selected_team} roster and performance")
                            
                            # Team Performance Overview
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Team Rank", team_data.get("rank", "N/A"))
                                st.metric("Conference", team_data.get("conf", "N/A"))
                            
                            with col2:
                                st.metric("Record", team_data.get("record", "N/A"))
                                st.metric("Win %", f"{(team_data.get('wins', 0) / (team_data.get('wins', 0) + team_data.get('losses', 1)) * 100):.1f}%")
                            
                            with col3:
                                st.metric("Offensive Rank", team_data.get("oe_rank", "N/A"))
                                st.metric("Defensive Rank", team_data.get("de_rank", "N/A"))
                            
                            with col4:
                                st.metric("Barthag Rating", f"{team_data.get('barthag', 0):.3f}")
                                st.metric("WAB", f"{team_data.get('WAB', 0):.1f}")
                            
                            st.markdown("---")
                            
                            # Roster Analysis (based on team data)
                            st.subheader("📋 Roster Analysis")
                            
                            # Performance Insights
                            st.write("**Team Performance Insights:**")
                            
                            # Offensive Analysis
                            adjoe = team_data.get("adjoe", 0)
                            if adjoe > 120:
                                st.write("• 🟢 **Strong Offensive Team** - High scoring efficiency")
                            elif adjoe > 110:
                                st.write("• 🟡 **Average Offensive Team** - Moderate scoring")
                            else:
                                st.write("• 🔴 **Offensive Challenges** - Below average scoring")
                            
                            # Defensive Analysis
                            adjde = team_data.get("adjde", 0)
                            if adjde < 95:
                                st.write("• 🟢 **Elite Defense** - Very low opponent scoring")
                            elif adjde < 105:
                                st.write("• 🟡 **Solid Defense** - Good defensive efficiency")
                            else:
                                st.write("• 🔴 **Defensive Concerns** - High opponent scoring")
                            
                            # Tempo Analysis
                            st.write("**Playing Style Analysis:**")
                            if adjoe > 120 and adjde > 105:
                                st.write("• ⚡ **High-Tempo Team** - Fast-paced, high-scoring games")
                            elif adjoe < 110 and adjde < 95:
                                st.write("• 🐌 **Slow-Tempo Team** - Defensive, low-scoring games")
                            else:
                                st.write("• ⚖️ **Balanced Team** - Moderate tempo and scoring")
                            
                            # Conference Context
                            st.write("**Conference Context:**")
                            conf = team_data.get("conf", "")
                            if conf:
                                # Get conference teams for comparison
                                conf_response = requests.get(f"{API_BASE_URL}/teams/search?query={conf}")
                                if conf_response.status_code == 200:
                                    conf_teams = conf_response.json().get("teams", [])
                                    if conf_teams:
                                        st.write(f"• **Conference**: {conf} ({len(conf_teams)} teams in database)")
                                        st.write(f"• **Conference Strength**: {team_data.get('sos', 0):.3f} SOS rating")
                            
                            st.markdown("---")
                            
                            # Player-Level Insights (Future Enhancement)
                            st.subheader("🔮 Player-Level Analysis (Future Enhancement)")
                            st.info("""
                            **Planned Features:**
                            • Individual player statistics and rankings
                            • Player efficiency ratings and usage rates
                            • Position-specific analysis (PG, SG, SF, PF, C)
                            • Player comparison tools
                            • Recruitment analytics and fit analysis
                            • Performance trends and development tracking
                            """)
                            
                        else:
                            st.error(f"Could not fetch data for {selected_team}")
                else:
                    st.warning(f"No teams found matching '{team_search}'")
        else:
            st.error("Could not fetch team list")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Try searching for a specific team to analyze their roster and performance.")

def show_game_preparation():
    """Display game preparation page."""
    st.header("Game Preparation & Scouting")
    
    st.markdown("---")
    
    # Opponent Selection
    st.subheader("🎯 Select Opponent for Scouting")
    
    # Get opponent team
    opponent_search = st.text_input("Search for opponent:", placeholder="e.g., Duke, Michigan, Purdue")
    
    if opponent_search:
        try:
            # Search for opponent
            response = requests.get(f"{API_BASE_URL}/teams/search?query={opponent_search}")
            if response.status_code == 200:
                opponents = response.json().get("teams", [])
                
                if opponents:
                    st.success(f"Found {len(opponents)} teams matching '{opponent_search}'")
                    
                    # Select opponent
                    opponent_options = [f"{team['team']} ({team['conference']})" for team in opponents]
                    selected_opponent_display = st.selectbox("Select opponent:", opponent_options)
                    
                    if selected_opponent_display:
                        opponent_name = selected_opponent_display.split(" (")[0]
                        
                        # Get opponent data
                        opponent_response = requests.get(f"{API_BASE_URL}/teams/{opponent_name}")
                        if opponent_response.status_code == 200:
                            opponent_data = opponent_response.json().get("team", {})
                            
                            st.markdown("---")
                            
                            # Automated Scouting Report
                            st.subheader("📋 Automated Scouting Report")
                            st.success(f"**Opponent**: {opponent_name} ({opponent_data.get('conf', 'N/A')})")
                            
                            # Key Statistics
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Rank", opponent_data.get("rank", "N/A"))
                                st.metric("Record", opponent_data.get("record", "N/A"))
                            
                            with col2:
                                st.metric("Offensive Rank", opponent_data.get("oe_rank", "N/A"))
                                st.metric("Defensive Rank", opponent_data.get("de_rank", "N/A"))
                            
                            with col3:
                                st.metric("AdjOE", f"{opponent_data.get('adjoe', 0):.1f}")
                                st.metric("AdjDE", f"{opponent_data.get('adjde', 0):.1f}")
                            
                            with col4:
                                st.metric("Barthag", f"{opponent_data.get('barthag', 0):.3f}")
                                st.metric("WAB", f"{opponent_data.get('WAB', 0):.1f}")
                            
                            st.markdown("---")
                            
                            # Strengths & Weaknesses Analysis
                            st.subheader("🔍 Strengths & Weaknesses")
                            
                            # Offensive Analysis
                            adjoe = opponent_data.get("adjoe", 0)
                            oe_rank = opponent_data.get("oe_rank", 999)
                            
                            st.write("**Offensive Analysis:**")
                            if adjoe > 120 and oe_rank < 50:
                                st.write("• 🟢 **STRENGTH**: Elite offensive efficiency")
                                st.write("• ⚠️ **CONCERN**: High-scoring opponent")
                            elif adjoe > 110:
                                st.write("• 🟡 **MODERATE**: Above-average offense")
                            else:
                                st.write("• 🔴 **WEAKNESS**: Below-average scoring")
                            
                            # Defensive Analysis
                            adjde = opponent_data.get("adjde", 0)
                            de_rank = opponent_data.get("de_rank", 999)
                            
                            st.write("**Defensive Analysis:**")
                            if adjde < 95 and de_rank < 50:
                                st.write("• 🟢 **WEAKNESS**: Poor defensive efficiency")
                                st.write("• ✅ **OPPORTUNITY**: Exploit defensive gaps")
                            elif adjde < 105:
                                st.write("• 🟡 **MODERATE**: Average defense")
                            else:
                                st.write("• 🔴 **STRENGTH**: Strong defensive team")
                            
                            # Tempo Analysis
                            st.write("**Tempo & Style:**")
                            if adjoe > 120 and adjde > 105:
                                st.write("• ⚡ **Fast-paced team** - Prepare for high-scoring game")
                                st.write("• 🏃‍♂️ **Strategy**: Control tempo, limit transition opportunities")
                            elif adjoe < 110 and adjde < 95:
                                st.write("• 🐌 **Slow-paced team** - Prepare for defensive battle")
                                st.write("• 🛡️ **Strategy**: Be patient, execute half-court offense")
                            else:
                                st.write("• ⚖️ **Balanced team** - Adapt to game flow")
                            
                            st.markdown("---")
                            
                            # Game Plan Suggestions
                            st.subheader("🎯 Game Plan Suggestions")
                            
                            # Defensive Strategy
                            st.write("**Defensive Strategy:**")
                            if adjoe > 120:
                                st.write("• 🛡️ **Focus on transition defense** - Limit fast breaks")
                                st.write("• 🎯 **Contest every shot** - High-scoring team")
                                st.write("• ⏱️ **Control pace** - Slow down their offense")
                            else:
                                st.write("• 🎯 **Pressure the ball** - Force turnovers")
                                st.write("• 🏀 **Rebound aggressively** - Limit second chances")
                            
                            # Offensive Strategy
                            st.write("**Offensive Strategy:**")
                            if adjde > 105:
                                st.write("• 🎯 **Be patient** - Strong defensive opponent")
                                st.write("• 🏀 **Attack the rim** - Draw fouls")
                                st.write("• ⏱️ **Use shot clock** - Find good shots")
                            else:
                                st.write("• ⚡ **Push the pace** - Exploit defensive weaknesses")
                                st.write("• 🎯 **Take open shots** - Capitalize on opportunities")
                            
                            st.markdown("---")
                            
                            # Matchup Analysis
                            st.subheader("⚔️ Matchup Analysis")
                            
                            # Get your team for comparison (assuming Illinois)
                            your_team = "Illinois"
                            comparison_response = requests.get(f"{API_BASE_URL}/teams/compare/{your_team}/{opponent_name}")
                            
                            if comparison_response.status_code == 200:
                                comparison = comparison_response.json().get("comparison", {})
                                comp_data = comparison.get("comparison", {})
                                
                                if comp_data:
                                    st.write(f"**{your_team} vs {opponent_name} Key Matchups:**")
                                    
                                    for metric, data in comp_data.items():
                                        if isinstance(data, dict):
                                            your_value = data.get('team1_value', 0)
                                            their_value = data.get('team2_value', 0)
                                            advantage = data.get('advantage', '')
                                            
                                            if metric == 'barthag':
                                                st.write(f"• **Overall Rating**: {your_team} ({your_value:.3f}) vs {opponent_name} ({their_value:.3f})")
                                                if advantage == 'team1':
                                                    st.write(f"  → **{your_team} advantage** - Higher overall rating")
                                                else:
                                                    st.write(f"  → **{opponent_name} advantage** - Higher overall rating")
                                            
                                            elif metric == 'adjoe':
                                                st.write(f"• **Offensive Efficiency**: {your_team} ({your_value:.1f}) vs {opponent_name} ({their_value:.1f})")
                                                if advantage == 'team1':
                                                    st.write(f"  → **{your_team} offensive advantage**")
                                                else:
                                                    st.write(f"  → **{opponent_name} offensive advantage**")
                                            
                                            elif metric == 'adjde':
                                                st.write(f"• **Defensive Efficiency**: {your_team} ({your_value:.1f}) vs {opponent_name} ({their_value:.1f})")
                                                if advantage == 'team1':
                                                    st.write(f"  → **{your_team} defensive advantage**")
                                                else:
                                                    st.write(f"  → **{opponent_name} defensive advantage**")
                            
                            st.markdown("---")
                            
                            # Future Enhancements
                            st.subheader("🔮 Advanced Features (Future Enhancement)")
                            st.info("""
                            **Planned Features:**
                            • Individual player scouting reports
                            • Historical matchup analysis
                            • Real-time game statistics
                            • Advanced analytics and predictions
                            • Video integration with statistics
                            • Custom scouting report generation
                            • In-game adjustment recommendations
                            """)
                            
                        else:
                            st.error(f"Could not fetch data for {opponent_name}")
                else:
                    st.warning(f"No teams found matching '{opponent_search}'")
            else:
                st.error("Error searching for opponent")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Enter an opponent team name to generate a scouting report and game plan.")

def show_data_sources():
    """Display data sources configuration."""
    st.header("Data Sources")
    
    st.subheader("Available Sources")
    
    # Test BartTorvik connection
    try:
        response = requests.get(f"{API_BASE_URL}/teams/search?query=Illinois")
        barttorvik_status = "✅ Connected" if response.status_code == 200 else "❌ Disconnected"
        barttorvik_data = response.json().get("teams", []) if response.status_code == 200 else []
    except:
        barttorvik_status = "❌ Disconnected"
        barttorvik_data = []
    
    # BartTorvik
    with st.expander("BartTorvik (T-Rank)", expanded=True):
        st.write(f"**Status**: {barttorvik_status}")
        st.write("**Description**: Primary source for team rankings and statistics")
        st.write("**Access**: Free CSV/JSON downloads")
        if barttorvik_data:
            st.write(f"**Data Available**: {len(barttorvik_data)} teams found for 'Illinois' search")
            st.write("**Sample Data**:")
            for team in barttorvik_data[:3]:
                st.write(f"  • {team['team']} ({team['conference']}) - {team['record']}")
    
    # KenPom
    with st.expander("KenPom"):
        st.write("**Status**: 🔄 Planned Integration")
        st.write("**Description**: Advanced basketball analytics")
        st.write("**Access**: Subscription required")
        st.write("**Note**: Will be integrated in future updates")
    
    # Sports Reference
    with st.expander("Sports Reference"):
        st.write("**Status**: 🔄 Planned Integration")
        st.write("**Description**: Backup source for additional metrics")
        st.write("**Access**: Web scraping")
        st.write("**Note**: Will be integrated in future updates")
    
    st.markdown("---")
    st.subheader("API Configuration")
    st.success(f"✅ Backend API: {API_BASE_URL}")
    st.info("Data is automatically fetched from BartTorvik through the backend API.")
    
    # Show API endpoints
    with st.expander("Available API Endpoints"):
        st.write("• `GET /teams/search?query={team_name}` - Search for teams")
        st.write("• `GET /teams/{team_name}` - Get team statistics")
        st.write("• `GET /teams/compare/{team1}/{team2}` - Compare two teams")
        st.write("• `GET /teams/list` - List all available teams")

if __name__ == "__main__":
    main()