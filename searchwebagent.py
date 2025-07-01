import os, openai
from dotenv import load_dotenv

load_dotenv()                               # ← loads the 2 vars
openai.api_key  = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_API_BASE")   # must end in /

# --- 1. list models so we know the correct IDs -------------
print("\n🔍 Available Groq models:")
for m in openai.models.list().data:
    print(" •", m.id)

# Pick one that actually appears (example: mixtral-8x7b-32768)
MODEL_ID = "mixtral-8x7b-32768"             # ← change if you saw a different ID above

# --- 2. send a chat ---------------------------------------
resp = openai.chat.completions.create(
    model=MODEL_ID,
    messages=[{
        "role": "user",
        "content": "Give me three summer-2025 trends in women’s fashion and homeware."
    }]
)
print("\n✅ Groq replied:\n")
print(resp.choices[0].message.content)
