# app.py
import os
import json
from collections import deque
from dotenv import load_dotenv
from openai import OpenAI
from mlb_query.function_schema import function_schema
from mlb_query.dispatcher import execute_function
from mlb_query.planner import plan_steps
from utils.selector import select_relevant_info
from utils.formatter import format_response_with_llm
from datetime import datetime

# ⭐ 读取.env文件
load_dotenv()

# ⭐ 全局debug buffer
_debug_buffer = []

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
today = datetime.now().strftime("%Y-%m-%d") 
def refine_query(history_results, next_step_instruction):
    """
    带着历史结果 + 下一步计划，细化出具体小query（可能多条）
    """
    prompt = f"""
你是一个MLB智能助手的小query补全器。

当前日期是：{today}

历史查询结果（按顺序累积）：
{json.dumps(history_results, ensure_ascii=False, indent=2)}

下一步计划动作：
"{next_step_instruction}"

要求：
- 综合历史结果，生成清晰、具体的小query
- 小query必须可以直接function_call，不留模糊或变量
- 如需生成多条小query，每行一条，换行分隔，不要使用列表或JSON格式
- 只输出小query文本，不要解释，不要加任何引号
- 如果历史结果中缺失关键信息，无法细化，请直接输出"该信息不可用，无法继续生成具体查询"
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    refined = response.choices[0].message.content.strip()

    print("\n[DEBUG] 动态细化小query：")
    print(refined)

    _debug_buffer.append(f"[细化小query]\n{refined}")

    refined_queries = [line.strip() for line in refined.splitlines() if line.strip()]
    return refined_queries

def run_conversation(user_input):
    global _debug_buffer
    _debug_buffer = []  # 每次运行前清空

    _debug_buffer.append(f"用户输入：{user_input}")

    # Step 1: 调用planner生成初步计划
    plan = plan_steps(user_input)
    if not plan:
        _debug_buffer.append("无法规划有效的查询步骤")
        return "很抱歉，无法规划有效的查询步骤。"

    task_queue = deque(plan)
    all_selected_data = []
    history_results = []

    # Step 2: 依次处理每个小query
    while task_queue:
        current_task = task_queue.popleft()
        mini_query = current_task["query"]
        depends_on_last = current_task["depends_on_last"]

        _debug_buffer.append(f"当前处理小query: {mini_query} (depends_on_last={depends_on_last})")

        if depends_on_last:
            refined_queries = refine_query(history_results, mini_query)

            if len(refined_queries) > 1:
                for q in reversed(refined_queries):
                    task_queue.appendleft({"query": q, "depends_on_last": False})
                continue
            elif refined_queries[0].startswith("该信息不可用"):
                _debug_buffer.append(f"无法继续处理: {mini_query}")
                all_selected_data.append({"info": f"无法继续处理: {mini_query}"})
                continue
            else:
                mini_query = refined_queries[0]

        _debug_buffer.append(f"最终执行小query: {mini_query}")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": mini_query}],
            functions=function_schema,
            function_call="auto"
        )

        message = response.choices[0].message

        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)

            _debug_buffer.append(f"调用function: {function_name}, 参数: {arguments}")

            raw_data = execute_function(function_name, arguments)
            _debug_buffer.append(f"查询原始结果: {raw_data}")

            selected_data = select_relevant_info(mini_query, raw_data)
            _debug_buffer.append(f"筛选后的数据: {selected_data}")

            all_selected_data.append(selected_data)
            history_results.append(selected_data)
        else:
            _debug_buffer.append(f"未能执行小query: {mini_query}")
            all_selected_data.append({"info": f"未能执行小query: {mini_query}"})

    # Step 3: 用formatter组织最终回答
    final_response = format_response_with_llm(user_input, all_selected_data)
    return final_response

def get_debug_log():
    """
    提供完整思考过程
    """
    return "\n".join(_debug_buffer)

if __name__ == "__main__":
    user_input = input("请输入你的问题：")
    result = run_conversation(user_input)
    print("\n[最终查询结果]：")
    print(result)
