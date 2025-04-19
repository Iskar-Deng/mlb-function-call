import requests

def get_team_info(team_name):
    """查询MLB球队基本信息"""
    url = "https://statsapi.mlb.com/api/v1/teams"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "查询球队列表失败"}

    teams = response.json().get("teams", [])
    for team in teams:
        if team["name"].lower() == team_name.lower():
            return team

    return {"error": "未找到球队信息"}
