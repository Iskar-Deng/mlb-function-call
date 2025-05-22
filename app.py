# app.py
from mlb_query.engine import run_conversation, get_debug_log

if __name__ == "__main__":
    user_input = input("请输入你的问题：")
    result = run_conversation(user_input)

    print("\n[最终查询结果]：")
    print(result)
