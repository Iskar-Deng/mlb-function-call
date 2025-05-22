import statsapi
from .tools import get_player_id, lookup_team_id

def get_team_info(team_name):
    """查询MLB球队基本信息"""
    teams = statsapi.lookup_team(team_name)
    return teams[0] if teams else {"error": f"未找到球队：{team_name}"}

def get_team_roster(team_name, season):
    """查询指定球队某赛季球员名单（结构化）"""
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"未找到球队：{team_name}"}
    
    roster = statsapi.roster(team_id, season=season)
    if not roster:
        return {"error": f"{team_name} 在 {season} 赛季没有找到球员名单"}

    return roster
