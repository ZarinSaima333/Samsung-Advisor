# test_gemini.py
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Did you create a .env file?")

# Initialize Gemini client
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = '''
You are RozaAI, a helpful assistant. Answer in JSON format:

{
"sql_query": "string"
}
'''

# Test question
question = "select all color phones from samsung"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
)

# Gemini response
print(response.choices[0].message.content)
