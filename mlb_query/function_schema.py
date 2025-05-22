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
        "name": "get_player_stats",
        "description": "查询MLB球员的打击、投球或防守数据（支持赛季和生涯）",
        "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "球员英文全名，例如 Shohei Ohtani"
                },
                "stat_type": {
                    "type": "string",
                    "enum": ["season", "career"],
                    "description": "统计类型，赛季或生涯"
                },
                "group": {
                    "type": "string",
                    "enum": ["hitting", "pitching", "fielding"],
                    "description": "数据类型：打击、投球或防守"
                },
                "season": {
                    "type": "integer",
                    "description": "赛季年份，例如 2024（仅当 stat_type 为 season 时需要）"
                }
            },
            "required": ["player_name", "stat_type", "group"]
        }
    },
    {
        "name": "get_team_leaders",
        "description": "获取球队在某一类别中的统计领先者",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {"type": "string", "description": "球队英文名称"},
                "category": {"type": "string", "description": "统计类别，如 'homeRuns', 'walks'"},
                "season": {"type": "integer", "description": "赛季年份，如 2025"},
                "limit": {"type": "integer", "description": "返回排名前几的球员，默认10"}
            },
            "required": ["team_name", "category", "season"]
        }
    },
    {
        "name": "get_league_leaders",
        "description": "获取联盟或全联盟某项数据的领先球员",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "统计类别，如 'onBasePlusSlugging', 'homeRuns'"},
                "season": {"type": "integer", "description": "赛季年份，如 2025"},
                "stat_group": {"type": "string", "description": "统计分组，如 'hitting', 'pitching', 'fielding'"},
                "league_id": {"type": "integer", "description": "联盟编号（103=AL，104=NL），可选"},
                "limit": {"type": "integer", "description": "返回前几名，默认10"}
            },
            "required": ["category", "season", "stat_group"]
        }
    },
    {
        "name": "get_team_standings",
        "description": "获取指定联盟和日期下的排名信息",
        "parameters": {
            "type": "object",
            "properties": {
                "league_id": {"type": "integer", "description": "联盟编号，如 103（美联）或104（国联）"},
                "date": {"type": "string", "description": "日期，格式为 MM/DD/YYYY，如 '05/21/2025'"}
            },
            "required": ["league_id", "date"]
        }
    }
]
