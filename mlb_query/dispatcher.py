from .functions.player import get_player_info, get_player_stats
from .functions.team import get_team_info, get_team_roster
from .functions.game import get_game_result, get_game_box_score
from .functions.league import get_league_leaders, get_team_standings, get_team_leaders

def execute_function(function_name, arguments):
    """
    Dispatch function: call the corresponding local function based on function_name.
    """

    if function_name == "get_player_info":
        return get_player_info(arguments["player_name"])

    elif function_name == "get_player_stats":
        return get_player_stats(
            player_name=arguments["player_name"],
            stat_type=arguments["stat_type"],
            group=arguments["group"],
            season=arguments.get("season")
        )

    elif function_name == "get_team_info":
        return get_team_info(arguments["team_name"])
    
    elif function_name == "get_team_roster":
        return get_team_roster(arguments["team_name"], arguments["season"])

    elif function_name == "get_game_result":
        return get_game_result(arguments["team_name"], arguments["date"])
    
    elif function_name == "get_game_box_score":
        return get_game_box_score(arguments["team_name"], arguments["date"])
    
    elif function_name == "get_team_leaders":
        return get_team_leaders(
            team_name=arguments["team_name"],
            category=arguments["category"],
            season=arguments["season"],
            limit=arguments.get("limit", 10)
        )

    elif function_name == "get_league_leaders":
        return get_league_leaders(
            category=arguments["category"],
            season=arguments["season"],
            stat_group=arguments["stat_group"],
            league_id=arguments.get("league_id"),
            limit=arguments.get("limit", 10)
        )

    elif function_name == "get_team_standings":
        return get_team_standings(
            league_id=arguments["league_id"],
            date=arguments["date"]
        )

    else:
        return {"error": f"Unrecognized function: {function_name}"}
