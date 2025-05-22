# utils/openai_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("未设置 OPENAI_API_KEY")
        _client = OpenAI(api_key=api_key)
    return _client
