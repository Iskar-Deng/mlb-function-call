import statsapi

def lookup_team_id(team_name):
    """根据队名查找 team_id"""
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return None
    return teams[0]['id']

def get_game_result(team_name, date):
    """
    查询指定球队在某天的比赛结果（简洁版）
    """
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"无法识别球队名称：{team_name}"}

    games = statsapi.schedule(start_date=date, end_date=date, team=team_id)
    if not games:
        return {"error": f"{team_name} 在 {date} 没有比赛"}

    game = games[0]
    return {
        "game_pk": game.get("game_id"),
        "date": game.get("game_date"),
        "home_team": game.get("home_name"),
        "away_team": game.get("away_name"),
        "home_score": game.get("home_score"),
        "away_score": game.get("away_score"),
        "status": game.get("status"),
        "summary": game.get("summary")
    }

def get_game_box_score(team_name, date):
    """
    查询指定球队在某日的比赛 box score（返回格式化文本 + gamePk，可用于联动）。
    """
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"未找到球队：{team_name}"}

    # 查找当天该队的比赛
    games = statsapi.schedule(start_date=date, end_date=date, team=team_id)
    if not games:
        return {"error": f"{team_name} 在 {date} 没有比赛"}

    game = games[0]
    game_pk = game.get("game_id")

    try:
        boxscore = statsapi.boxscore(
            game_pk,
            battingBox=True,
            battingInfo=True,
            fieldingInfo=True,
            pitchingBox=True,
            gameInfo=True
        )
    except Exception as e:
        return {"error": f"获取 box score 失败: {str(e)}"}

    return {
        "game_pk": game_pk,
        "date": game.get("game_date"),
        "home_team": game.get("home_name"),
        "away_team": game.get("away_name"),
        "boxscore_text": boxscore
    }
