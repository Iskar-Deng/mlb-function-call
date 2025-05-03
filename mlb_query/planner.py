import os
from openai import OpenAI
from datetime import datetime  # <-- 新增导入

FUNCTION_CATALOG = """
你可以使用以下功能（只能基于这些功能规划小query，不要创造新功能）：

get_player_info：查询球员基本资料，需要参数：player_name（球员英文全名）
get_team_info：查询球队基本信息，需要参数：team_name（球队英文全称）
get_team_roster：查询指定球队某个赛季的球员名单，需要参数：team_name，season
get_player_career_stats：查询球员生涯总体打击数据，需要参数：player_name（球员英文全名）
get_player_career_pitching_stats：查询球员生涯投球数据，需要参数：player_name（球员英文全名）
get_player_season_stats：查询球员某个赛季的打击数据，需要参数：player_name，season
get_team_game_on_date：查询某一天某球队的比赛，返回比赛信息（包含比赛id），需要参数：team_name，date
get_team_games_in_range：查询某时间段某球队的比赛，返回比赛信息列表，需要参数：team_name，start_date，end_date
get_game_box_score：查询球队某天的比赛box score，需要参数：team_name，date
get_game_highlights：查询指定比赛的高光视频，需要参数：game_pk（比赛id）

"""

def plan_steps(user_input):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 初始化放到函数里面
    """
    粗粒度规划，返回步骤列表（每步带depends_on_last标记）
    """

    today = datetime.now().strftime("%Y-%m-%d")  # <-- 获取今天日期

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

功能列表：
{FUNCTION_CATALOG}

示例（严格模仿格式）：
查询Mookie Betts的基本资料 false
确认Mookie Betts效力过Red Sox和Dodgers的年份 true
针对Red Sox期间的每个赛季，查询Mookie Betts的打击数据 true
针对Dodgers期间的每个赛季，查询Mookie Betts的打击数据 true

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
