import requests
import pandas as pd
from typing import Optional, Dict, List
import os
from datetime import datetime

class BartTorvik:
    def __init__(self):
        self.base_url = os.getenv("BARTTORVIK_BASE_URL", "https://barttorvik.com")
        self.current_year = datetime.now().year
        
    def get_team_results(self, year: Optional[int] = None) -> pd.DataFrame:
        """Fetch team results from BartTorvik for a given year"""
        if year is None:
            year = self.current_year
            
        url = f"{self.base_url}/{year}_team_results.csv"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Read CSV data into DataFrame
            from io import StringIO
            df = pd.read_csv(StringIO(response.text))
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from BartTorvik: {e}")
            return pd.DataFrame()
    
    def get_team_by_name(self, team_name: str, year: Optional[int] = None) -> Optional[Dict]:
        """Get specific team data by name"""
        df = self.get_team_results(year)
        
        if df.empty:
            return None
            
        # Search for team (case insensitive)
        team_data = df[df['Team'].str.contains(team_name, case=False, na=False)]
        
        if team_data.empty:
            return None
            
        return team_data.iloc[0].to_dict()
    
    def get_opponent_comparison(self, team1: str, team2: str, year: Optional[int] = None) -> Dict:
        """Compare two teams' statistics"""
        df = self.get_team_results(year)
        
        if df.empty:
            return {}
            
        team1_data = df[df['Team'].str.contains(team1, case=False, na=False)]
        team2_data = df[df['Team'].str.contains(team2, case=False, na=False)]
        
        if team1_data.empty or team2_data.empty:
            return {}
            
        team1_stats = team1_data.iloc[0].to_dict()
        team2_stats = team2_data.iloc[0].to_dict()
        
        return {
            "team1": team1_stats,
            "team2": team2_stats,
            "comparison": self._generate_comparison(team1_stats, team2_stats)
        }
    
    def _generate_comparison(self, team1: Dict, team2: Dict) -> Dict:
        """Generate comparison metrics between two teams"""
        comparison = {}
        
        # Key metrics to compare
        metrics = [
            'barthag', 'adjoe', 'adjde', 'adjte', 'efg_o', 'efg_d', 
            'tov_o', 'tov_d', 'or_o', 'or_d', 'ftr_o', 'ftr_d'
        ]
        
        for metric in metrics:
            if metric in team1 and metric in team2:
                try:
                    val1 = float(team1[metric])
                    val2 = float(team2[metric])
                    comparison[metric] = {
                        "team1_value": val1,
                        "team2_value": val2,
                        "difference": val1 - val2,
                        "advantage": "team1" if val1 > val2 else "team2"
                    }
                except (ValueError, TypeError):
                    continue
                    
        return comparison
    
    def get_available_teams(self, year: Optional[int] = None) -> List[str]:
        """Get list of all available teams"""
        df = self.get_team_results(year)
        
        if df.empty:
            return []
            
        return df['Team'].tolist()
    
    def search_teams(self, query: str, year: Optional[int] = None) -> List[Dict]:
        """Search for teams by partial name match"""
        df = self.get_team_results(year)
        
        if df.empty:
            return []
            
        matching_teams = df[df['Team'].str.contains(query, case=False, na=False)]
        
        return [
            {
                "team": row['Team'],
                "conference": row.get('Conference', 'Unknown'),
                "record": f"{row.get('wins', 0)}-{row.get('losses', 0)}",
                "barthag": row.get('barthag', 0)
            }
            for _, row in matching_teams.iterrows()
        ]