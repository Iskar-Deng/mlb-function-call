import requests

def get_player_info(player_name):
    """查询MLB球员基本资料"""
    url = f"https://statsapi.mlb.com/api/v1/people/search?names={player_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "查询球员资料失败"}

    data = response.json().get("people", [])
    if not data:
        return {"error": "未找到球员信息"}

    return data[0]

def get_player_season_stats(player_name, season):
    """查询MLB球员某赛季打击数据"""
    player_info = get_player_info(player_name)
    if "id" not in player_info:
        return {"error": "未找到球员ID"}

    player_id = player_info["id"]
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season={season}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "查询球员赛季数据失败"}

    stats = response.json().get("stats", [])
    if not stats or not stats[0].get("splits"):
        return {"error": "暂无该赛季数据"}

    return stats[0]["splits"][0]["stat"]
