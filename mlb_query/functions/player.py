import statsapi
from .tools import get_player_id, lookup_team_id

def get_player_info(player_name):
    """Query basic MLB player information."""
    players = statsapi.lookup_player(player_name)
    if not players:
        return {"error": "Player not found"}
    
    player = players[0]
    return player

def get_player_stats(player_name, stat_type="season", group="hitting", season=None):
    """
    Retrieve MLB player statistics, supporting hitting/pitching/fielding,
    and either season or career data.

    Parameters:
    - player_name (str): Full name of the player
    - stat_type (str): Either "season" or "career"
    - group (str): One of "hitting", "pitching", or "fielding"
    - season (int or None): Required if stat_type is "season"

    Returns:
    - dict: Player statistics or error message
    """
    player_id = get_player_id(player_name)
    if not player_id:
        return {"error": "Player not found"}

    if stat_type == "season" and not season:
        return {"error": "Parameter 'season' is required for season stats"}

    stats = statsapi.player_stat_data(
        player_id,
        group=group,
        type=stat_type,
        season=season if stat_type == "season" else None
    )

    return stats.get("stats", {"error": f"No {stat_type} / {group} data available"})
