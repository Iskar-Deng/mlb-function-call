import statsapi

def get_player_id(player_name):
    players = statsapi.lookup_player(player_name)
    if not players:
        return None
    return players[0]['id']

def lookup_team_id(team_name):
    """根据队名查找 team_id"""
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return None
    return teams[0]['id']
