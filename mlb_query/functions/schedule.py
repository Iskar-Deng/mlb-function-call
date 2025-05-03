import statsapi

def get_team_game_on_date(team_name, date):
    """
    查询某一天某球队的比赛
    """
    try:
        games = statsapi.schedule(date=date, team=team_name)
    except Exception as e:
        return {"error": f"查询失败: {str(e)}"}

    if not games:
        return {"message": f"{team_name} 在 {date} 没有比赛"}

    game_list = []
    for game in games:
        game_list.append({
            "game_id": game['game_id'],
            "summary": game['summary'],
            "status": game['status']
        })

    return {
        "team": team_name,
        "date": date,
        "games": game_list
    }

def get_team_games_in_range(team_name, start_date, end_date):
    """
    查询某时间段某球队的比赛
    """
    try:
        games = statsapi.schedule(start_date=start_date, end_date=end_date, team=team_name)
    except Exception as e:
        return {"error": f"查询失败: {str(e)}"}

    if not games:
        return {"message": f"{team_name} 在 {start_date} 到 {end_date} 没有比赛"}

    game_list = []
    for game in games:
        game_list.append({
            "game_id": game['game_id'],
            "summary": game['summary'],
            "status": game['status']
        })

    return {
        "team": team_name,
        "start_date": start_date,
        "end_date": end_date,
        "games": game_list
    }