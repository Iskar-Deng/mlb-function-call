import requests
from datetime import datetime

def get_game_result(team_name, date):
    """查询指定球队某天的比赛结果"""
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={formatted_date}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "查询比赛结果失败"}

    dates = response.json().get("dates", [])
    if not dates:
        return {"error": "该日期无比赛数据"}

    games = dates[0].get("games", [])
    for game in games:
        teams = game["teams"]
        home_team = teams["home"]["team"]["name"]
        away_team = teams["away"]["team"]["name"]

        if team_name.lower() in [home_team.lower(), away_team.lower()]:
            return {
                "date": date,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": teams["home"]["score"],
                "away_score": teams["away"]["score"],
                "status": game["status"]["detailedState"]
            }

    return {"error": "未找到相关比赛"}
