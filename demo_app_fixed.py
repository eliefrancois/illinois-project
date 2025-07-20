"""
Simplified College Basketball Scouting Dashboard using available BartTorvik data.
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
        
        # Handle duplicate column names properly
        csv_text = response.text
        lines = csv_text.split('\n')
        
        # Parse header and fix duplicate column names
        header_line = lines[0].strip()
        header_cols = header_line.split(',')
        
        # Fix duplicate 'rank' columns
        seen_cols = {}
        fixed_header = []
        for col in header_cols:
            if col in seen_cols:
                seen_cols[col] += 1
                fixed_header.append(f"{col}_{seen_cols[col]}")
            else:
                seen_cols[col] = 0
                fixed_header.append(col)
        
        # Rebuild CSV with fixed header
        lines[0] = ','.join(fixed_header)
        fixed_csv = '\n'.join(lines)
        
        df = pd.read_csv(StringIO(fixed_csv))
        
        # Parse record into wins and losses
        if 'record' in df.columns:
            df[['wins', 'losses']] = df['record'].str.split('-', expand=True).astype(int)
        
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
            st.metric("Record", f"{team_data.get('wins', 0)}-{team_data.get('losses', 0)}")
            st.metric("Rank", f"#{team_data.get('rank', 'N/A')}")
    
    with col2:
        if selected_team:
            st.subheader(f"📈 {selected_team} Detailed Analysis")
            
            # Key metrics
            metrics_cols = st.columns(3)
            
            with metrics_cols[0]:
                st.markdown("**Offense**")
                st.write(f"Adj. Efficiency: {team_data.get('adjoe', 0):.1f}")
                st.write(f"Offensive Rank: #{team_data.get('oe Rank', 'N/A')}")
                if 'Con Adj OE' in team_data:
                    st.write(f"Conference OE: {team_data.get('Con Adj OE', 0):.1f}")
            
            with metrics_cols[1]:
                st.markdown("**Defense**")
                st.write(f"Adj. Efficiency: {team_data.get('adjde', 0):.1f}")
                st.write(f"Defensive Rank: #{team_data.get('de Rank', 'N/A')}")
                if 'Con Adj DE' in team_data:
                    st.write(f"Conference DE: {team_data.get('Con Adj DE', 0):.1f}")
            
            with metrics_cols[2]:
                st.markdown("**Schedule**")
                st.write(f"SOS: {team_data.get('sos', 0):.2f}")
                st.write(f"Non-Con SOS: {team_data.get('ncsos', 0):.2f}")
                st.write(f"Conference: {team_data.get('conf', 'Unknown')}")
                if 'WAB' in team_data:
                    st.write(f"WAB: {team_data.get('WAB', 0):.1f}")
            
            # Simple performance chart
            create_team_performance_chart(team_data, selected_team, df)

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
        metrics = ['barthag', 'adjoe', 'adjde', 'sos', 'wins', 'losses']
        
        comparison_df = pd.DataFrame({
            'Metric': ['BartTorvik Rating', 'Adj. Offense', 'Adj. Defense', 'Strength of Schedule', 'Wins', 'Losses'],
            team1: [team1_data.get(m, 0) for m in metrics],
            team2: [team2_data.get(m, 0) for m in metrics]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        # Side-by-side performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            create_team_performance_chart(team1_data, team1, df)
        
        with col2:
            create_team_performance_chart(team2_data, team2, df)

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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_barthag = conf_df['barthag'].mean()
        st.metric("Avg BartTorvik Rating", f"{avg_barthag:.3f}")
    
    with col2:
        avg_offense = conf_df['adjoe'].mean()
        st.metric("Avg Adj. Offense", f"{avg_offense:.1f}")
    
    with col3:
        avg_defense = conf_df['adjde'].mean()
        st.metric("Avg Adj. Defense", f"{avg_defense:.1f}")
    
    with col4:
        total_wins = conf_df['wins'].sum()
        st.metric("Total Conference Wins", f"{total_wins}")
    
    # Top teams in conference
    st.subheader("Top Teams by BartTorvik Rating")
    top_teams = conf_df.nlargest(10, 'barthag')[['team', 'barthag', 'adjoe', 'adjde', 'record']]
    st.dataframe(top_teams, use_container_width=True)
    
    # Conference distribution chart
    fig = px.scatter(conf_df, x='adjoe', y='adjde', hover_name='team', 
                    title=f"{selected_conf} - Offensive vs Defensive Efficiency",
                    labels={'adjoe': 'Adjusted Offensive Efficiency', 'adjde': 'Adjusted Defensive Efficiency'})
    st.plotly_chart(fig, use_container_width=True)

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
        rank = team_data.get('rank', 999)
        
        # Strengths and weaknesses
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Strengths**")
            strengths = []
            
            if adjoe > df['adjoe'].quantile(0.75):
                strengths.append("Elite offensive efficiency")
            if adjde < df['adjde'].quantile(0.25):
                strengths.append("Dominant defensive performance")
            if rank <= 25:
                strengths.append("Top 25 ranked team")
            if barthag > df['barthag'].quantile(0.80):
                strengths.append("High overall team rating")
            if team_data.get('sos', 0) > df['sos'].quantile(0.75):
                strengths.append("Tested against strong schedule")
            
            for strength in strengths:
                st.write(f"• {strength}")
            
            if not strengths:
                st.write("• Solid overall performance")
        
        with col2:
            st.markdown("**🔴 Areas of Concern**")
            weaknesses = []
            
            if adjoe < df['adjoe'].quantile(0.25):
                weaknesses.append("Struggles with offensive efficiency")
            if adjde > df['adjde'].quantile(0.75):
                weaknesses.append("Defensive efficiency concerns")
            if rank > 100:
                weaknesses.append("Lower national ranking")
            if team_data.get('sos', 0) < df['sos'].quantile(0.25):
                weaknesses.append("Weak strength of schedule")
            
            for weakness in weaknesses:
                st.write(f"• {weakness}")
            
            if not weaknesses:
                st.write("• No major weaknesses identified")
        
        # Game plan suggestions
        st.markdown("**🎯 Game Plan Suggestions**")
        
        game_plan = []
        
        if adjoe > df['adjoe'].quantile(0.75):
            game_plan.append("Focus on defensive intensity - they have strong offense")
        
        if adjde > df['adjde'].quantile(0.75):
            game_plan.append("Attack their defense - they struggle defensively")
        
        if team_data.get('sos', 0) < df['sos'].quantile(0.30):
            game_plan.append("They may not be tested - apply early pressure")
        
        if not game_plan:
            game_plan.append("Balanced approach - they're well-rounded")
        
        for suggestion in game_plan:
            st.write(f"• {suggestion}")
        
        # Team ranking context
        st.markdown("**📊 National Context**")
        st.write(f"• National Rank: #{rank}")
        st.write(f"• BartTorvik Rating: {barthag:.3f} (Percentile: {(df['barthag'] < barthag).mean() * 100:.0f}%)")
        st.write(f"• Offensive Efficiency: {adjoe:.1f} (Percentile: {(df['adjoe'] < adjoe).mean() * 100:.0f}%)")
        st.write(f"• Defensive Efficiency: {adjde:.1f} (Percentile: {(df['adjde'] > adjde).mean() * 100:.0f}%)")

def create_team_performance_chart(team_data, team_name, df):
    """Create a simple bar chart showing team performance percentiles"""
    
    # Calculate percentiles
    barthag_pct = (df['barthag'] < team_data.get('barthag', 0)).mean() * 100
    offense_pct = (df['adjoe'] < team_data.get('adjoe', 0)).mean() * 100
    defense_pct = (df['adjde'] > team_data.get('adjde', 0)).mean() * 100  # Lower is better for defense
    
    metrics = ['Overall Rating', 'Offensive Efficiency', 'Defensive Efficiency']
    percentiles = [barthag_pct, offense_pct, defense_pct]
    
    fig = go.Figure(data=[
        go.Bar(x=metrics, y=percentiles, 
               marker_color=['lightblue', 'lightgreen', 'lightcoral'])
    ])
    
    fig.update_layout(
        title=f"{team_name} Performance Percentiles",
        yaxis_title="Percentile vs All Teams",
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()