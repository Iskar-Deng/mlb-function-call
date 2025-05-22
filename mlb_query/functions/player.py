import statsapi
from .tools import get_player_id, lookup_team_id

def get_player_info(player_name):
    """查询MLB球员基本资料"""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "未找到球员信息"}
    
    player = players[0]
    return player

def get_player_stats(player_name, stat_type="season", group="hitting", season=None):
    """
    查询MLB球员的打击 / 投球 / 防守数据，支持赛季和生涯。

    参数说明：
    - player_name: 球员全名
    - stat_type: "season" or "career"
    - group: "hitting" / "pitching" / "fielding"
    - season: 可选，赛季年份（stat_type=season 时必填）
    """
    player_id = get_player_id(player_name)
    if not player_id:
        return {"error": "未找到球员信息"}

    if stat_type == "season" and not season:
        return {"error": "查询赛季数据时必须提供 season 参数"}

    stats = statsapi.player_stat_data(
        player_id,
        group=group,
        type=stat_type,
        season=season if stat_type == "season" else None
    )

    return stats.get("stats", {"error": f"暂无 {stat_type} / {group} 数据"})
