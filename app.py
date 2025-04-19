import os
import json
from collections import deque
from openai import OpenAI
from mlb_query.function_schema import function_schema
from mlb_query.dispatcher import execute_function
from mlb_query.planner import plan_steps
from utils.selector import select_relevant_info
from utils.formatter import format_response_with_llm

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def refine_query(previous_result, next_step_instruction):
    """
    带着上一步查询结果，结合下一步动作描述，生成具体小query（可能多条）
    """
    prompt = f"""
你是一个MLB智能助手的小query补全器。

上一步查询结果：
{json.dumps(previous_result, ensure_ascii=False, indent=2)}

下一步计划动作：
"{next_step_instruction}"

要求：
- 根据上一步结果和动作描述，生成清晰、具体的小query
- 小query必须可以直接function_call，不留模糊或变量
- 如果需要生成多条小query，请每行一条，换行分隔，不要使用JSON或列表格式
- 只输出小query文本，不要解释，不要加任何标点或引号
- 如果上一步查询结果中缺少关键信息，请不要凭空补全，直接返回"该信息不可用，无法继续生成具体查询"。
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    refined = response.choices[0].message.content.strip()

    print("\n[DEBUG] 动态细化小query：")
    print(refined)

    # 判断是否是多条小query
    refined_queries = [line.strip() for line in refined.splitlines() if line.strip()]
    return refined_queries

def run_conversation(user_input):
    print("\n[DEBUG] 用户输入：", user_input)

    # Step 1: 调用planner生成初步计划
    plan = plan_steps(user_input)
    if not plan:
        return "很抱歉，无法规划有效的查询步骤。"

    task_queue = deque(plan)
    all_selected_data = []
    last_result = {}

    # Step 2: 遍历每一个小query
    while task_queue:
        current_task = task_queue.popleft()
        mini_query = current_task["query"]
        depends_on_last = current_task["depends_on_last"]

        print(f"\n[DEBUG] 当前处理小query: {mini_query} (depends_on_last={depends_on_last})")

        if depends_on_last:
            refined_queries = refine_query(last_result, mini_query)

            if len(refined_queries) > 1:
                # 如果细化出了多条小query，压回队列，优先执行
                for q in reversed(refined_queries):
                    task_queue.appendleft({"query": q, "depends_on_last": False})
                continue  # 当前task不执行，继续处理压进去的
            else:
                mini_query = refined_queries[0]

        print(f"[DEBUG] 最终执行小query: {mini_query}")

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

            print(f"[DEBUG] 调用function: {function_name}, 参数: {arguments}")

            raw_data = execute_function(function_name, arguments)
            print("[DEBUG] 查询原始结果:", raw_data)

            selected_data = select_relevant_info(mini_query, raw_data)
            print("[DEBUG] 筛选后的数据:", selected_data)

            all_selected_data.append(selected_data)
            last_result = selected_data

        else:
            print("[DEBUG] 无法function_call，记录文本")
            all_selected_data.append({"info": f"未能执行小query: {mini_query}"})

    # Step 3: 汇总回答
    final_response = format_response_with_llm(user_input, all_selected_data)

    return final_response

if __name__ == "__main__":
    user_input = input("请输入你的问题：")
    result = run_conversation(user_input)
    print("\n[最终查询结果]：")
    print(result)
