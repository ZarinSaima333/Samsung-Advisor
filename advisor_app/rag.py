# rag.py
from openai import OpenAI
import os
from sqlalchemy import text

from database import get_db
from model import SamsungDevice
from sqlalchemy.orm import Session
import json
import re

API_KEY = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = '''
You are a SQL query generator. Given a natural language question, output a JSON with a single field "sql_query".

Table: samsung_devices
Columns:
id, model, series, device_type, release_date, display_inches, battery_mah,
battery_type, camera_main_mp, price_value, price_currency, price_usd, price_bdt, storage, source_url

Output Format:
{
  "sql_query": "SQL query string here"
}

Example:
Q: What is the price of Samsung Galaxy A07?
A: {"sql_query": "SELECT model, price_usd, price_bdt FROM samsung_devices WHERE model = 'Samsung Galaxy A07';"}

Q: Which one has bigger display in samsung Z series?
A: {"sql_query": "SELECT model, display_inches FROM samsung_devices WHERE series = 'Z' ORDER BY display_inches DESC LIMIT 1;"}

Q: What is the latest samsung phone?
A: {"sql_query": "SELECT model, release_date FROM samsung_devices ORDER BY release_date DESC LIMIT 1;"}
'''



def generate_sql_and_fetch(question: str, db: Session):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    gemini_output = response.choices[0].message.content
    print("Gemini output:", gemini_output)

    try:
        sql_dict = json.loads(gemini_output)
        sql_query = sql_dict.get("sql_query")
    except:
        match = re.search(r'"sql_query"\s*:\s*"(.*?)"', gemini_output, re.DOTALL)
        sql_query = match.group(1) if match else None

    if not sql_query:
        print("❌ Failed to extract SQL")
        return []

    try:
        result = db.execute(text(sql_query)).mappings().all()
        return result
    except Exception as e:
        print("❌ SQL execution error:", e)
        return []
