import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FUNCTION_CATALOG = """
你可以使用以下功能（只能基于这些功能规划小query，不要创造新功能）：

1. get_player_info：查询球员基本资料，需要参数：player_name（球员英文全名）
2. get_player_season_stats：查询球员某个赛季的打击数据，需要参数：player_name，season
3. get_team_info：查询球队基本信息，需要参数：team_name（球队英文全称）
4. get_game_result：查询某支球队在某天的比赛结果，需要参数：team_name，date
"""

def plan_steps(user_input):
    """
    粗粒度规划，返回步骤列表（每步带depends_on_last标记）
    """
    prompt = f"""
你是一个MLB智能助手的任务规划器。

你的任务是基于以下已支持的功能，制定一个合理的查询步骤列表。

要求：
- 每行写一个小query + 一个true/false，表示这步是否依赖上一步查询的结果
- 格式严格为：自然语言描述 [空格] true/false
- 不能生成JSON或列表，只是纯文本！
- 如果无法利用已有功能完成，请输出："该功能暂未实现" false
- 不能使用自己的常识，一切信息必须来源于查询
- 默认查询2025年赛季

功能列表：
{FUNCTION_CATALOG}

示例（请严格模仿这个格式）：
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
