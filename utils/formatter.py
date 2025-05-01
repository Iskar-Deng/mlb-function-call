from openai import OpenAI
import os
import json

def format_response_with_llm(user_input, selected_data_list):
    """
    根据用户原始问题以及各个小查询的筛选结果，
    生成自然、流畅且用户友好的最终回答。
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 初始化放到函数里面
    prompt = f"""
你是一个专业的MLB数据分析助手。

用户的问题是：
{user_input}

以下是根据用户问题查询到的相关信息：
{json.dumps(selected_data_list, ensure_ascii=False, indent=2)}

请你根据这些信息，生成一段清晰、完整、自然语言的回答：

要求：
- 回答简洁明了，清晰易读。
- 若数据不完整或未能完全满足用户需求，礼貌地指出。

直接给出自然语言回答即可，不需要额外解释。
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    final_reply = response.choices[0].message.content.strip()

    return final_reply
