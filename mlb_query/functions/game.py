import statsapi

def get_game_box_score(team_name, date):
    """
    Retrieve the formatted box score for a team's MLB game on a specific date.

    Args:
        team_name (str): Full name of the team in English (e.g., "Yankees")
        date (str): Date of the game in YYYY-MM-DD format

    Returns:
        dict: A formatted boxscore string or an error message.
    """
    schedule = statsapi.schedule(date=date, sportId=1)
    if not schedule:
        return {"error": f"No games found on {date}"}

    game_pk = None
    for game in schedule:
        home = game['home_name'].strip().lower()
        away = game['away_name'].strip().lower()
        if team_name.strip().lower() in [home, away]:
            game_pk = game['game_id']
            break

    if not game_pk:
        return {"error": f"No game found for {team_name} on {date}"}

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
        return {"error": f"Failed to retrieve boxscore: {str(e)}"}

    return {
        "date": date,
        "team": team_name,
        "boxscore_text": boxscore
    }

def lookup_team_id(team_name):
    """Lookup the numeric team_id based on a team name."""
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return None
    return teams[0]['id']

def get_game_result(team_name, date):
    """
    Retrieve the game result for a specific team on a given date.

    Args:
        team_name (str): Full team name in English
        date (str): Date in YYYY-MM-DD format

    Returns:
        dict: Game result summary or error message.
    """
    team_id = lookup_team_id(team_name)
    if not team_id:
        return {"error": f"Could not identify team: {team_name}"}

    games = statsapi.schedule(start_date=date, end_date=date, team=team_id)
    if not games:
        return {"error": f"No game found for {team_name} on {date}"}

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

