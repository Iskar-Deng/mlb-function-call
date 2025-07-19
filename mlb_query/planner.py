import os
from openai import OpenAI
from datetime import datetime

FUNCTION_CATALOG = """
You may use the following functions (you must not create new ones):

get_player_info: Query basic player information. Required parameter: player_name (full name in English)
get_team_info: Query basic team information. Required parameter: team_name (full name in English)
get_team_roster: Query a team's player list for a given season. Required parameters: team_name, season
get_player_career_stats: Query a player's career batting stats. Required parameter: player_name
get_player_career_pitching_stats: Query a player's career pitching stats. Required parameter: player_name
get_player_season_stats: Query a player's batting stats for a specific season. Required parameters: player_name, season
get_team_game_on_date: Query a team's game on a specific date. Required parameters: team_name, date
get_team_games_in_range: Query a team's games within a given date range. Required parameters: team_name, start_date, end_date
get_game_box_score: Query the box score for a team's game on a specific date. Required parameters: team_name, date
"""

def plan_steps(user_input):
    """
    Plan a high-level step list based on the user's question.
    Each step includes whether it depends on the previous step.
    Returns: list of {"query": ..., "depends_on_last": bool}
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are the planning module of an MLB assistant.

Today's date is: {today}

Your task is to generate a sequence of query steps based on the user's question,
using only the supported functions below.

Instructions:
- Each line must contain a natural language subquery followed by a space and then 'true' or 'false'
- Format strictly: subquery description [space] true/false
- Do not output lists or JSON
- If the functionality is not supported, write: "false"
- Do not use world knowledge — rely only on available queries
- Default to current season if not specified

Supported functions:
{FUNCTION_CATALOG}

Example (follow format strictly):
Query basic info about Mookie Betts false
Find the years Mookie Betts played for Red Sox and Dodgers true
For each Red Sox season, get Mookie Betts's batting stats true
For each Dodgers season, get Mookie Betts's batting stats true

User question:
"{user_input}"

Output the planned steps, one per line.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    plan_text = response.choices[0].message.content.strip()

    print("\n[DEBUG] Planned step list:")
    print(plan_text)

    steps = []
    for line in plan_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            query_part, depends_part = line.rsplit(' ', 1)
            depends_on_last = depends_part.lower() == 'true'
            steps.append({
                "query": query_part,
                "depends_on_last": depends_on_last
            })
        except Exception as e:
            print("[ERROR] Failed to parse planner output:", e)
            return None

    return steps
