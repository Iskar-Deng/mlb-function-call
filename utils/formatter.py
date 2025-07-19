from openai import OpenAI
import os
import json

def format_response_with_llm(user_input, selected_data_list):
    """
    Generates a final natural language answer based on the user's original question
    and the selected data from subqueries.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
You are a professional MLB data assistant.

The user's question is:
{user_input}

The following is the information retrieved from various subqueries:
{json.dumps(selected_data_list, ensure_ascii=False, indent=2)}

Please generate a clear, concise, and natural-language answer based on the information above.

Requirements:
- Keep the answer simple and easy to read
- If data is incomplete or partially missing, politely point it out

Only output the final answer in natural language, no additional explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    final_reply = response.choices[0].message.content.strip()
    return final_reply
