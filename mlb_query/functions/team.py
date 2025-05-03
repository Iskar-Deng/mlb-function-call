import statsapi

def get_team_info(team_name):
    """查询MLB球队基本信息"""
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return {"error": "未找到球队信息"}
    
    team = teams[0]
    return team

def get_team_roster(team_name, season):
    """查询指定球队某个赛季的球员名单"""
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return {"error": "未找到球队信息"}
    
    team_id = teams[0]['id']
    
    roster_list = statsapi.roster(team_id, season=season)
    if not roster_list:
        return {"error": "未找到该赛季名单"}

    # 格式化输出
    return roster_list
