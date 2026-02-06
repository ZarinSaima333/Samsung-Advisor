# llm.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are a Samsung smartphone expert and tech reviewer.

Your task:
- Analyze structured phone data provided as JSON
- Answer the user's question in natural language
- Provide comparisons, recommendations, or explanations
- Be concise but informative
- If data is missing, say it clearly
- Do NOT hallucinate specs
- If other inforamtive you have related to the phone model say but dont hallucinate. 
-use you knowledge about information needed for best camera etc(if needed)
- if all info is asked don't blanty give all information comparatively answer, and for such cases keep your answer between 5-6 lines.
Output ONLY plain text (no JSON, no markdown).



"""

from datetime import date, datetime
from decimal import Decimal

def generate_answer(question: str, db_rows: list):
    """
    Agent 2: Converts DB rows + question into a human-friendly answer
    """

    if not db_rows:
        return "I couldn’t find enough data in the database to answer this question."

    # ✅ Convert RowMapping → dict and make all values JSON serializable
    serializable_rows = []
    for row in db_rows:
        safe_row = {}
        for k, v in dict(row).items():
            if isinstance(v, (date, datetime)):
                safe_row[k] = v.isoformat()      # convert dates to string
            elif isinstance(v, Decimal):
                safe_row[k] = float(v)          # convert Decimal to float
            else:
                safe_row[k] = v
        serializable_rows.append(safe_row)

    user_prompt = f"""
User Question:
{question}

Database Rows (JSON):
{json.dumps(serializable_rows, indent=2)}

Now generate a helpful answer for the user.
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()