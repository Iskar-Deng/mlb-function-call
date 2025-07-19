function_schema = [
    {
        "name": "get_player_info",
        "description": "Query basic profile of an MLB player.",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "Full name of the player in English. Example: 'Shohei Ohtani'"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_team_info",
        "description": "Query basic information of an MLB team.",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Full English name of the team. Example: 'Baltimore Orioles'"
                }
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_game_result",
        "description": "Get the result of a specific game for a team on a given date.",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Full English name of the team. Example: 'Seattle Mariners'"
                },
                "date": {
                    "type": "string",
                    "description": "Date of the game in YYYY-MM-DD format. Example: '2025-04-18'"
                }
            },
            "required": ["team_name", "date"]
        }
    },
    {
        "name": "get_team_roster",
        "description": "Retrieve the player roster of a team for a specific season.",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Full team name. Example: 'Boston Red Sox'"
                },
                "season": {
                    "type": "integer",
                    "description": "Year of the season. Example: 2025"
                }
            },
            "required": ["team_name", "season"]
        }
    },
    {
        "name": "get_game_box_score",
        "description": "Get the formatted box score for a specific game.",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Full name of the team"
                },
                "date": {
                    "type": "string",
                    "description": "Game date in YYYY-MM-DD format"
                }
            },
            "required": ["team_name", "date"]
        }
    },
    {
        "name": "get_player_stats",
        "description": "Query a player's season or career stats.",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "Full name of the player. Example: 'Shohei Ohtani'"
                },
                "stat_type": {
                    "type": "string",
                    "enum": ["season", "career"],
                    "description": "Stat type: 'season' or 'career'"
                },
                "group": {
                    "type": "string",
                    "enum": ["hitting", "pitching", "fielding"],
                    "description": "Stat group: hitting / pitching / fielding"
                },
                "season": {
                    "type": "integer",
                    "description": "Season year. Required when stat_type is 'season'"
                }
            },
            "required": ["player_name", "stat_type", "group"]
        }
    },
    {
        "name": "get_team_leaders",
        "description": "Get top players in a statistical category for a team.",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Team name"
                },
                "category": {
                    "type": "string",
                    "description": "Stat category (e.g., 'homeRuns', 'walks')"
                },
                "season": {
                    "type": "integer",
                    "description": "Season year (e.g., 2025)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top players to return (default 10)"
                }
            },
            "required": ["team_name", "category", "season"]
        }
    },
    {
        "name": "get_league_leaders",
        "description": "Get top players in the league for a specific category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Stat category (e.g., 'onBasePlusSlugging', 'homeRuns')"
                },
                "season": {
                    "type": "integer",
                    "description": "Season year (e.g., 2025)"
                },
                "stat_group": {
                    "type": "string",
                    "description": "Stat group: hitting / pitching / fielding"
                },
                "league_id": {
                    "type": "integer",
                    "description": "League ID (103 = AL, 104 = NL) — optional"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top players to return (default 10)"
                }
            },
            "required": ["category", "season", "stat_group"]
        }
    },
    {
        "name": "get_team_standings",
        "description": "Query standings for a league on a specific date.",
        "parameters": {
            "type": "object",
            "properties": {
                "league_id": {
                    "type": "integer",
                    "description": "League ID (103 = AL, 104 = NL)"
                },
                "date": {
                    "type": "string",
                    "description": "Date in MM/DD/YYYY format (e.g., '05/21/2025')"
                }
            },
            "required": ["league_id", "date"]
        }
    }
]
