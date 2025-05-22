import os
from openai import OpenAI
from datetime import datetime

FUNCTION_CATALOG = """
你可以使用以下功能（只能基于这些功能规划小query，不要创造新功能）：

1. get_player_info：查询球员基本资料，需要参数：
   - player_name（球员英文全名）

2. get_player_stats：查询球员打击、投球或防守数据（支持赛季或生涯）
   - 参数：
     - player_name（球员英文全名）
     - stat_type：只能是 "season" 或 "career"
     - group：只能是 "hitting"（打击）、"pitching"（投球）、"fielding"（防守）
     - season（当 stat_type 为 season 时必填，例：2024）

3. get_team_info：查询球队基本信息，需要参数：
   - team_name（球队英文全称）

4. get_team_roster：查询指定球队某个赛季的球员名单，需要参数：
   - team_name（球队英文全称）
   - season（赛季年份）

5. get_game_result：查询指定MLB球队某天的比赛结果，需要参数：
   - team_name（球队英文全称）
   - date（格式为 YYYY-MM-DD）

6. get_game_box_score：查询某支球队在某天的比赛box score（详细结果），需要参数：
   - team_name（球队英文全称）
   - date（格式为 YYYY-MM-DD）

7. get_team_leaders：获取某支球队在某项数据（如全垒打、保送等）上的领先球员，需参数：
   - team_name（球队英文名）
   - category（统计字段，如 homeRuns、walks，英文全称）
   - season（赛季年份）

8. get_league_leaders：获取整个联盟在某项数据中的领先球员，需参数：
   - category（如 battingAverage，英文全称）
   - season（如 2024）
   - stat_group（hitting/pitching/fielding）

9. get_team_standings：获取某联盟（国联或美联）在指定日期下的排名，需参数：
   - league_id（103 = AL，104 = NL）
   - date（格式 MM/DD/YYYY）
"""

def plan_steps(user_input):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
你是一个MLB智能助手的任务规划器。

当前日期是：{today}

你的任务是基于以下已支持的功能，制定一个合理的查询步骤列表。

要求：
- 每行写一个小query + 一个true/false，表示这步是否依赖上一步查询的结果
- 格式严格为：自然语言描述 [空格] true/false
- 不能生成JSON或列表，只是纯文本！
- 如果无法利用已有功能完成，请输出："该功能暂未实现" false
- 不能使用自己的常识，一切信息必须来源于查询
- 默认查询当前赛季
- 请尽量根据已有功能，实现出用户需求

功能列表：
{FUNCTION_CATALOG}

示例（严格模仿格式）：
查询Mookie Betts的基本资料 false
查询Mookie Betts的2024赛季打击数据 false
查询Mookie Betts的2024赛季防守数据 false
查询Boston Red Sox在2024年的球员名单 false

用户问题：
"{user_input}"

请输出规划好的步骤，每行一句。
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    plan_text = response.choices[0].message.content.strip()

    print("\n[DEBUG] planner粗粒度步骤列表:")
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
            print("[ERROR] 解析planner输出失败:", e)
            return None

    return steps
