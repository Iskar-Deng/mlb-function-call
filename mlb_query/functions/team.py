import statsapi
from .tools import get_player_id, lookup_team_id

def get_team_info(team_name):
    """Query basic information about an MLB team."""
    teams = statsapi.lookup_team(team_name)
    return teams[0] if teams else {"error": f"Team not found: {team_name}"}

def get_team_roster(team_name, season):
    """Query the structured player roster of a team for a specific MLB season."""
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"Team not found: {team_name}"}
    
    roster = statsapi.roster(team_id, season=season)
    if not roster:
        return {"error": f"No roster found for {team_name} in season {season}"}

    return roster
