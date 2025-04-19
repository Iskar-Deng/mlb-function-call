import requests

def get_game_result(team_name, date):
    """查询指定球队某天比赛结果"""
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch schedule info"}

    data = response.json()
    games = data.get("dates", [{}])[0].get("games", [])
    if not games:
        return {"error": "No games found for that date"}

    # 查找对应球队的比赛
    for game in games:
        teams = game.get("teams", {})
        home = teams.get("home", {}).get("team", {}).get("name", "")
        away = teams.get("away", {}).get("team", {}).get("name", "")

        if team_name in [home, away]:
            # 比赛状态
            status = game.get("status", {}).get("detailedState", "Unknown")

            # 可能没有score信息（比如比赛未开始）
            home_score = teams.get("home", {}).get("score")
            away_score = teams.get("away", {}).get("score")

            return {
                "date": date,
                "home_team": home,
                "away_team": away,
                "home_score": home_score if home_score is not None else "N/A",
                "away_score": away_score if away_score is not None else "N/A",
                "status": status
            }

    return {"error": "No matching game for the specified team"}
