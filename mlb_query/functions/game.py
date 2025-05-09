import statsapi

def get_game_box_score(team_name, date):
    """
    用 statsapi 查询指定日期某支球队的 Box Score（完整格式化版）
    """
    # 查当天所有比赛
    schedule = statsapi.schedule(date=date, sportId=1)
    if not schedule:
        return {"error": f"{date} 没有找到比赛"}

    # 找到 gamePk
    game_pk = None
    for game in schedule:
        home = game['home_name'].strip().lower()
        away = game['away_name'].strip().lower()
        if team_name.strip().lower() in [home, away]:
            game_pk = game['game_id']
            break

    if not game_pk:
        return {"error": f"没有找到 {team_name} 在 {date} 的比赛"}

    # 调用 statsapi.boxscore 拿到格式化文本
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
        return {"error": f"获取 boxscore 失败: {str(e)}"}

    # 返回格式化好的文本（前端可以直接展示，也可以进一步处理）
    return {
        "date": date,
        "team": team_name,
        "boxscore_text": boxscore
    }
    
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