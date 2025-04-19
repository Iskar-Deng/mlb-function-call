from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def select_relevant_info(mini_query, raw_data):
    """
    根据小query和查询返回的raw_data，提取最相关的关键信息。
    使用大模型进行信息筛选。
    """

    prompt = f"""
你是一个数据筛选助手，任务是根据查询意图，从API原始数据中筛选出有用的信息。

小查询：
{mini_query}

原始数据：
{json.dumps(raw_data, ensure_ascii=False, indent=2)}

要求：
- 返回的信息精炼，直接相关小查询意图。
- 不要返回任何无关或多余信息。

请直接返回精炼后的JSON格式信息，不要其他解释。
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response.choices[0].message.content.strip()

    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        return {"info": result_text}
