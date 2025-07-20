"""
Standalone demo of College Basketball Scouting Dashboard with direct BartTorvik integration.
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="College Basketball Scouting Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def fetch_barttorvik_data(year=2025):
    """Fetch team data from BartTorvik"""
    url = f"https://barttorvik.com/{year}_team_results.csv"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def main():
    st.title("🏀 College Basketball Scouting Dashboard")
    st.markdown("**Real-time opponent analysis using BartTorvik data**")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🔧 Configuration")
        year = st.selectbox("Season", [2025, 2024, 2023], index=0)
        
        st.markdown("---")
        st.header("📊 Analysis Tools")
        page = st.selectbox(
            "Select Tool",
            ["Team Lookup", "Team Comparison", "Conference Analysis", "Scouting Report"]
        )
    
    # Load data
    with st.spinner("Loading current season data..."):
        df = fetch_barttorvik_data(year)
    
    if df.empty:
        st.error("Unable to load data. Please check your internet connection.")
        return
    
    st.success(f"✅ Loaded data for {len(df)} teams from {year} season")
    
    if page == "Team Lookup":
        show_team_lookup(df)
    elif page == "Team Comparison":
        show_team_comparison(df)
    elif page == "Conference Analysis":
        show_conference_analysis(df)
    elif page == "Scouting Report":
        show_scouting_report(df)

def show_team_lookup(df):
    st.header("🔍 Team Lookup")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        team_options = [""] + sorted(df['team'].tolist())
        selected_team = st.selectbox("Select Team", team_options)
        
        if selected_team:
            team_data = df[df['team'] == selected_team].iloc[0]
            
            st.subheader("Quick Stats")
            st.metric("BartTorvik Rating", f"{team_data.get('barthag', 0):.3f}")
            st.metric("Adj. Offensive Efficiency", f"{team_data.get('adjoe', 0):.1f}")
            st.metric("Adj. Defensive Efficiency", f"{team_data.get('adjde', 0):.1f}")
            
            if 'wins' in team_data and 'losses' in team_data:
                st.metric("Record", f"{team_data['wins']}-{team_data['losses']}")
    
    with col2:
        if selected_team:
            st.subheader(f"📈 {selected_team} Detailed Analysis")
            
            # Key metrics
            metrics_cols = st.columns(3)
            
            with metrics_cols[0]:
                st.markdown("**Offensive Stats**")
                st.write(f"Effective FG%: {team_data.get('efg_o', 0):.1f}%")
                st.write(f"Turnover Rate: {team_data.get('tov_o', 0):.1f}%")
                st.write(f"Offensive Rebounding: {team_data.get('or_o', 0):.1f}%")
                st.write(f"Free Throw Rate: {team_data.get('ftr_o', 0):.1f}%")
            
            with metrics_cols[1]:
                st.markdown("**Defensive Stats**")
                st.write(f"Opp Effective FG%: {team_data.get('efg_d', 0):.1f}%")
                st.write(f"Opp Turnover Rate: {team_data.get('tov_d', 0):.1f}%")
                st.write(f"Def Rebounding: {100-team_data.get('or_d', 0):.1f}%")
                st.write(f"Opp Free Throw Rate: {team_data.get('ftr_d', 0):.1f}%")
            
            with metrics_cols[2]:
                st.markdown("**Advanced**")
                st.write(f"Tempo: {team_data.get('adjte', 0):.1f}")
                st.write(f"Conference: {team_data.get('conf', 'Unknown')}")
                
            # Radar chart
            create_team_radar_chart(team_data, selected_team)

def show_team_comparison(df):
    st.header("⚖️ Team Comparison")
    
    col1, col2 = st.columns(2)
    
    team_options = [""] + sorted(df['team'].tolist())
    
    with col1:
        team1 = st.selectbox("Team 1", team_options, key="team1")
    
    with col2:
        team2 = st.selectbox("Team 2", team_options, key="team2")
    
    if team1 and team2 and team1 != team2:
        team1_data = df[df['team'] == team1].iloc[0]
        team2_data = df[df['team'] == team2].iloc[0]
        
        st.subheader(f"📊 {team1} vs {team2}")
        
        # Comparison metrics
        metrics = ['barthag', 'adjoe', 'adjde', 'adjte', 'efg_o', 'efg_d', 'tov_o', 'tov_d']
        
        comparison_df = pd.DataFrame({
            'Metric': ['BartTorvik Rating', 'Adj. Offense', 'Adj. Defense', 'Tempo', 
                      'Effective FG%', 'Opp Effective FG%', 'Turnover Rate', 'Opp TO Rate'],
            team1: [team1_data.get(m, 0) for m in metrics],
            team2: [team2_data.get(m, 0) for m in metrics]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        # Side-by-side radar charts
        col1, col2 = st.columns(2)
        
        with col1:
            create_team_radar_chart(team1_data, team1)
        
        with col2:
            create_team_radar_chart(team2_data, team2)

def show_conference_analysis(df):
    st.header("🏆 Conference Analysis")
    
    if 'conf' not in df.columns:
        st.warning("Conference data not available in current dataset")
        return
    
    conference_options = ["All"] + sorted(df['conf'].dropna().unique().tolist())
    selected_conf = st.selectbox("Select Conference", conference_options)
    
    if selected_conf == "All":
        conf_df = df
        st.subheader("All Teams")
    else:
        conf_df = df[df['conf'] == selected_conf]
        st.subheader(f"{selected_conf} Conference")
    
    # Conference stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_barthag = conf_df['barthag'].mean()
        st.metric("Avg BartTorvik Rating", f"{avg_barthag:.3f}")
    
    with col2:
        avg_offense = conf_df['adjoe'].mean()
        st.metric("Avg Adj. Offense", f"{avg_offense:.1f}")
    
    with col3:
        avg_defense = conf_df['adjde'].mean()
        st.metric("Avg Adj. Defense", f"{avg_defense:.1f}")
    
    # Top teams in conference
    st.subheader("Top Teams by BartTorvik Rating")
    top_teams = conf_df.nlargest(10, 'barthag')[['team', 'barthag', 'adjoe', 'adjde']]
    st.dataframe(top_teams, use_container_width=True)

def show_scouting_report(df):
    st.header("📋 Automated Scouting Report")
    
    team_options = [""] + sorted(df['team'].tolist())
    selected_team = st.selectbox("Select Team to Scout", team_options)
    
    if selected_team:
        team_data = df[df['team'] == selected_team].iloc[0]
        
        st.subheader(f"Scouting Report: {selected_team}")
        
        # Generate basic scouting insights
        barthag = team_data.get('barthag', 0)
        adjoe = team_data.get('adjoe', 0)
        adjde = team_data.get('adjde', 0)
        tempo = team_data.get('adjte', 0)
        
        # Strengths and weaknesses
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Strengths**")
            strengths = []
            
            if adjoe > df['adjoe'].quantile(0.75):
                strengths.append("Strong offensive efficiency")
            if adjde < df['adjde'].quantile(0.25):
                strengths.append("Elite defensive efficiency")
            if tempo > df['adjte'].quantile(0.75):
                strengths.append("High-tempo offense")
            if team_data.get('efg_o', 0) > df['efg_o'].quantile(0.75):
                strengths.append("Excellent shooting efficiency")
            
            for strength in strengths:
                st.write(f"• {strength}")
            
            if not strengths:
                st.write("• Average across all metrics")
        
        with col2:
            st.markdown("**🔴 Areas of Concern**")
            weaknesses = []
            
            if adjoe < df['adjoe'].quantile(0.25):
                weaknesses.append("Struggles with offensive efficiency")
            if adjde > df['adjde'].quantile(0.75):
                weaknesses.append("Defensive efficiency concerns")
            if team_data.get('tov_o', 0) > df['tov_o'].quantile(0.75):
                weaknesses.append("High turnover rate")
            if team_data.get('efg_d', 0) > df['efg_d'].quantile(0.75):
                weaknesses.append("Allows efficient shooting")
            
            for weakness in weaknesses:
                st.write(f"• {weakness}")
            
            if not weaknesses:
                st.write("• No major weaknesses identified")
        
        # Game plan suggestions
        st.markdown("**🎯 Game Plan Suggestions**")
        
        game_plan = []
        
        if team_data.get('tov_d', 0) > df['tov_d'].quantile(0.75):
            game_plan.append("Apply pressure defense - they force turnovers")
        
        if team_data.get('or_o', 0) > df['or_o'].quantile(0.75):
            game_plan.append("Box out aggressively - they're strong on offensive glass")
        
        if tempo < df['adjte'].quantile(0.25):
            game_plan.append("Push tempo - they prefer slower pace")
        
        for suggestion in game_plan:
            st.write(f"• {suggestion}")

def create_team_radar_chart(team_data, team_name):
    """Create a radar chart for team performance"""
    
    categories = ['Offense', 'Defense', 'Shooting', 'Rebounding', 'Ball Security']
    
    # Normalize values to 0-100 scale for visualization
    offense_score = min(100, max(0, (team_data.get('adjoe', 100) - 80) * 5))
    defense_score = min(100, max(0, (120 - team_data.get('adjde', 100)) * 5))
    shooting_score = min(100, max(0, (team_data.get('efg_o', 45) - 35) * 5))
    rebounding_score = min(100, max(0, team_data.get('or_o', 25) * 3))
    ball_security_score = min(100, max(0, (25 - team_data.get('tov_o', 20)) * 5))
    
    values = [offense_score, defense_score, shooting_score, rebounding_score, ball_security_score]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=team_name,
        line_color='blue'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"{team_name} Performance Radar",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()