
from dotenv import load_dotenv
from openai import OpenAI
import openai
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Please set OPENAI_API_KEY in your environment or in a .env file")

client = OpenAI(api_key=api_key)

# Allow overriding the model via env; sensible default but change if you prefer
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
payload = {"model": model, "messages": [{"role": "user", "content": "<>"}]}

try:
    response = client.chat.completions.create(**payload)
    print(response.choices[0].message.content)
except openai.RateLimitError:
    print("Request failed: insufficient quota or rate limit reached.")
    print("Check your OpenAI billing/usage at https://platform.openai.com/account/usage and consider switching to a model you have quota for (set OPENAI_MODEL), or top up your plan.")
    raise SystemExit(2)
except Exception as e:
    # Generic fallback to surface a short error message
    print(f"Request failed: {type(e).__name__}: {e}")
    raise
print(response.choices[0].message.content)