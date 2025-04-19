from .functions.player import get_player_info, get_player_season_stats
from .functions.team import get_team_info
from .functions.game import get_game_result

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

    else:
        return {"error": f"未识别的function: {function_name}"}
