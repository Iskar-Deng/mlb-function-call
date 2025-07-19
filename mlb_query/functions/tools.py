import statsapi

def get_player_id(player_name):
    """
    Look up the player ID using the player's full name.

    Args:
        player_name (str): Full name of the player (e.g., "Shohei Ohtani").

    Returns:
        int or None: The player's ID if found, otherwise None.
    """
    players = statsapi.lookup_player(player_name)
    if not players:
        return None
    return players[0]['id']

def lookup_team_id(team_name):
    """
    Look up the team ID using the team's full name.

    Args:
        team_name (str): Full name of the team (e.g., "Seattle Mariners").

    Returns:
        int or None: The team's ID if found, otherwise None.
    """
    teams = statsapi.lookup_team(team_name)
    if not teams:
        return None
    return teams[0]['id']
