import statsapi
from .tools import lookup_team_id

def get_team_leaders(team_name, category, season, limit=10):
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"未找到球队: {team_name}"}
    try:
        return statsapi.team_leaders(team_id, category, season=season, limit=limit)
    except Exception as e:
        return {"error": str(e)}

def get_league_leaders(category, season, stat_group, league_id=None, limit=10):
    try:
        return statsapi.league_leaders(
            leaderCategories=category,
            statGroup=stat_group,
            season=season,
            leagueId=league_id,
            limit=limit
        )
    except Exception as e:
        return {"error": str(e)}

def get_team_standings(league_id, date):
    try:
        return statsapi.standings(leagueId=league_id, date=date)
    except Exception as e:
        return {"error": str(e)}