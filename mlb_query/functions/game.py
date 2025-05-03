import statsapi

def get_game_result(team_name, date):
    """查询指定球队某天比赛结果"""
    games = statsapi.schedule(start_date=date, end_date=date)
    if not games:
        return {"error": "当天没有比赛"}

    for game in games:
        home = game['home_name']
        away = game['away_name']

        if team_name.lower() in [home.lower(), away.lower()]:
            status = game.get('status', 'Unknown')
            home_score = game.get('home_score', 'N/A')
            away_score = game.get('away_score', 'N/A')

            return {
                "date": date,
                "home_team": home,
                "away_team": away,
                "home_score": home_score,
                "away_score": away_score,
                "status": status
            }

    return {"error": "未找到该队的比赛"}

def get_game_highlights(game_pk):
    """
    获取给定 gamePk 的高光视频链接
    """
    try:
        highlights = statsapi.game_highlights(game_pk)
        if not highlights:
            return {"error": f"没有找到 gamePk {game_pk} 的高光视频"}
    except Exception as e:
        return {"error": f"获取高光视频失败: {str(e)}"}

    # 整理成清单形式
    highlight_list = []
    for item in highlights:
        highlight_list.append({
            "title": item.get('title', '无标题'),
            "blurb": item.get('blurb', ''),
            "duration": item.get('duration', ''),
            "url": item.get('playbacks', [{}])[0].get('url', '无链接')
        })

    return {
        "game_pk": game_pk,
        "highlights": highlight_list
    }