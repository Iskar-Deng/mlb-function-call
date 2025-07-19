import os
import json
from collections import deque
from dotenv import load_dotenv
from openai import OpenAI
from mlb_query.function_schema import function_schema
from mlb_query.dispatcher import execute_function
from mlb_query.planner import plan_steps
from utils.formatter import format_response_with_llm
from datetime import datetime

# ⭐ Load environment variables
load_dotenv()

# ⭐ Global debug buffer
_debug_buffer = []

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
today = datetime.now().strftime("%Y-%m-%d")

def refine_query(history_results, next_step_instruction):
    """
    Refines a query based on past results and the next planned action.
    If multiple refined queries are generated, returns them as a list.
    If required info is missing, returns a message indicating the failure.
    """
    prompt = f"""
You are a query refiner for an MLB assistant.

Today's date is: {today}

Past results (in order):
{json.dumps(history_results, ensure_ascii=False, indent=2)}

Next planned action:
"{next_step_instruction}"

Instructions:
- Use the history to generate clear, concrete subqueries
- The subqueries must be directly function-callable, no ambiguity or placeholders
- If generating multiple subqueries, output one per line (plain text), no list or JSON
- Output only the query text, no explanation or quotes
- If required info is missing, output: "The information is not available for this query"
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    refined = response.choices[0].message.content.strip()

    print("\n[DEBUG] Refined subqueries:")
    print(refined)

    _debug_buffer.append(f"[Refined subqueries]\n{refined}")

    refined_queries = [line.strip() for line in refined.splitlines() if line.strip()]
    return refined_queries

def run_conversation(user_input):
    """
    Main entry point for running a full query workflow.
    Steps:
    1. Plan tasks using the planner.
    2. Execute subqueries, handle dependencies.
    3. Format and return the final response.
    """
    global _debug_buffer
    _debug_buffer = []  # Reset debug log
    _debug_buffer.append(f"User input: {user_input}")

    # Step 1: Plan subqueries
    plan = plan_steps(user_input)
    if not plan:
        _debug_buffer.append("Failed to generate query plan.")
        return "Sorry, unable to generate a valid query plan."

    task_queue = deque(plan)
    all_selected_data = []
    history_results = []

    # Step 2: Execute each subquery
    while task_queue:
        current_task = task_queue.popleft()
        mini_query = current_task["query"]
        depends_on_last = current_task["depends_on_last"]

        _debug_buffer.append(f"Processing subquery: {mini_query} (depends_on_last={depends_on_last})")

        if depends_on_last:
            refined_queries = refine_query(history_results, mini_query)

            if len(refined_queries) > 1:
                for q in reversed(refined_queries):
                    task_queue.appendleft({"query": q, "depends_on_last": False})
                continue
            elif refined_queries[0].startswith("The imformation is not available"):
                _debug_buffer.append(f"Cannot proceed with: {mini_query}")
                all_selected_data.append({"info": f"Cannot proceed with: {mini_query}"})
                continue
            else:
                mini_query = refined_queries[0]

        _debug_buffer.append(f"Final subquery to execute: {mini_query}")

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

            _debug_buffer.append(f"Calling function: {function_name}, Arguments: {arguments}")

            raw_data = execute_function(function_name, arguments)
            _debug_buffer.append(f"Raw result: {raw_data}")

            all_selected_data.append(raw_data)
            history_results.append(raw_data)
        else:
            _debug_buffer.append(f"Failed to execute subquery: {mini_query}")
            all_selected_data.append({"info": f"Failed to execute subquery: {mini_query}"})

    # Step 3: Format final response
    final_response = format_response_with_llm(user_input, all_selected_data)
    return final_response

def get_debug_log():
    """
    Returns full debug log of the reasoning process.
    """
    return "\n".join(_debug_buffer)

if __name__ == "__main__":
    user_input = input("Enter your question: ")
    result = run_conversation(user_input)
    print("\n[Final Response]:")
    print(result)
