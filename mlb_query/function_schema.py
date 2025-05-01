function_schema = [
    {
        "name": "get_player_info",
        "description": "查询MLB球员的基本资料",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "球员英文全名，例如 Shohei Ohtani"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_player_season_stats",
        "description": "查询MLB球员在指定赛季的打击数据",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "球员英文全名，例如 Shohei Ohtani"
                },
                "season": {
                    "type": "integer",
                    "description": "赛季年份，例如 2024"
                }
            },
            "required": ["player_name", "season"]
        }
    },
    {
        "name": "get_team_info",
        "description": "查询MLB球队基本信息",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "球队英文全称，例如 Baltimore Orioles"
                }
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_game_result",
        "description": "查询指定MLB球队某天的比赛结果",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "球队英文全称，例如 Seattle Mariners"
                },
                "date": {
                    "type": "string",
                    "description": "比赛日期，格式YYYY-MM-DD，例如 2025-04-18"
                }
            },
            "required": ["team_name", "date"]
        }
    },
    {
        "name": "get_player_career_stats",
        "description": "查询球员生涯的打击统计数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "球员的英文全名，例如 'Mookie Betts'"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_player_career_pitching_stats",
        "description": "查询球员生涯投球数据",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "球员的英文全名，如 'Clayton Kershaw'"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_team_roster",
        "description": "查询指定球队某个赛季的球员名单",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "球队英文全称，例如 Boston Red Sox"
                },
                "season": {
                    "type": "integer",
                    "description": "赛季年份，例如2025"
                }
            },
            "required": ["team_name", "season"]
        }
    },
    {
        "name": "get_game_box_score",
        "description": "查询某支球队在某天的比赛box score",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {"type": "string", "description": "球队英文全称"},
                "date": {"type": "string", "description": "比赛日期，格式YYYY-MM-DD"}
            },
            "required": ["team_name", "date"]
        }
    },
        {
        "name": "get_game_highlights",
        "description": "获取指定比赛的高光视频链接",
        "parameters": {
            "type": "object",
            "properties": {
                "game_pk": {"type": "integer"}
            },
            "required": ["game_pk"]
        }
    }
]
