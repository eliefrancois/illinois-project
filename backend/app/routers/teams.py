from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..services.barttorvik_service import BartTorvik

router = APIRouter(prefix="/teams", tags=["teams"])
bt_service = BartTorvik()

@router.get("/search")
async def search_teams(
    query: str = Query(..., description="Team name to search for"),
    year: Optional[int] = Query(None, description="Year (default: current year)")
):
    """Search for teams by name"""
    try:
        results = bt_service.search_teams(query, year)
        return {"teams": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching teams: {str(e)}")

@router.get("/list")
async def get_all_teams(
    year: Optional[int] = Query(None, description="Year (default: current year)")
):
    """Get list of all available teams"""
    try:
        teams = bt_service.get_available_teams(year)
        return {"teams": teams}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching teams: {str(e)}")

@router.get("/{team_name}")
async def get_team_stats(
    team_name: str,
    year: Optional[int] = Query(None, description="Year (default: current year)")
):
    """Get detailed statistics for a specific team"""
    try:
        team_data = bt_service.get_team_by_name(team_name, year)
        
        if not team_data:
            raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")
            
        return {"team": team_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team data: {str(e)}")

@router.get("/compare/{team1}/{team2}")
async def compare_teams(
    team1: str,
    team2: str,
    year: Optional[int] = Query(None, description="Year (default: current year)")
):
    """Compare statistics between two teams"""
    try:
        comparison = bt_service.get_opponent_comparison(team1, team2, year)
        
        if not comparison:
            raise HTTPException(
                status_code=404, 
                detail=f"One or both teams not found: '{team1}', '{team2}'"
            )
            
        return {"comparison": comparison}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing teams: {str(e)}")