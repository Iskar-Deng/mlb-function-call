import statsapi

def get_player_info(player_name):
    """查询MLB球员基本资料"""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "未找到球员信息"}
    
    player = players[0]
    return player

def get_player_season_stats(player_name, season):
    """查询MLB球员某赛季打击数据"""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "未找到球员信息"}
    
    player_id = players[0]['id']
    stats = statsapi.player_stat_data(player_id, group='hitting', type='season', season=season)
    
    if not stats or 'stats' not in stats:
        return {"error": "暂无该赛季数据"}
    
    return stats['stats']

def get_player_career_stats(player_name):
    """查询MLB球员整个生涯的打击数据"""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "未找到球员信息"}
    
    player_id = players[0]['id']
    stats = statsapi.player_stat_data(player_id, group='hitting', type='career')
    
    if not stats or 'stats' not in stats:
        return {"error": "暂无生涯打击数据"}
    
    return stats['stats']

def get_player_career_pitching_stats(player_name):
    """查询MLB球员整个生涯的投球数据"""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "未找到球员信息"}
    
    player_id = players[0]['id']
    stats = statsapi.player_stat_data(player_id, group='pitching', type='career')
    
    if not stats or 'stats' not in stats:
        return {"error": "暂无生涯投球数据"}
    
    return stats['stats']
