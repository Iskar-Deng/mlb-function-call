from .functions.player import get_player_info, get_player_season_stats, get_player_career_stats, get_player_career_pitching_stats
from .functions.team import get_team_info, get_team_roster
from .functions.game import get_game_box_score, get_game_highlights
from .functions.schedule import get_team_game_on_date, get_team_games_in_range

def execute_function(function_name, arguments):
    """
    根据function_name调用对应的本地function
    """
    if function_name == "get_player_info":
        return get_player_info(arguments["player_name"])

    elif function_name == "get_player_season_stats":
        return get_player_season_stats(arguments["player_name"], arguments["season"])

    elif function_name == "get_team_info":
        return get_team_info(arguments["team_name"])

    elif function_name == "get_game_result":
        return get_game_result(arguments["team_name"], arguments["date"])
    
    elif function_name == "get_player_career_stats":
        return get_player_career_stats(arguments["player_name"])
    
    elif function_name == "get_player_career_pitching_stats":
        return get_player_career_pitching_stats(arguments["player_name"])
    
    elif function_name == "get_team_roster":
        return get_team_roster(arguments["team_name"], arguments["season"])
    
    elif function_name == "get_game_box_score":
        return get_game_box_score(arguments["team_name"], arguments["date"])

    elif function_name == "get_game_highlights":
        return get_game_highlights(arguments["game_pk"])
    
    elif function_name == "get_team_game_on_date":
        return get_team_game_on_date(arguments["team_name"], arguments["date"])
    
    elif function_name == "get_team_games_in_range":
        return get_team_games_in_range(arguments["team_name"], arguments["start_date"], arguments["end_date"])

    else:
        return {"error": f"未识别的function: {function_name}"}
