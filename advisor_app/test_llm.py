# test_llm.py
from llm import generate_answer

# Fake DB rows (simulate output from RAG)
sample_rows = [
    {
        "model": "Samsung Galaxy S23 Ultra",
        "display_inches": 6.8,
        "battery_mah": 5000,
        "camera_main_mp": 200,
        "price_usd": 1199
    },
    {
        "model": "Samsung Galaxy S22 Ultra",
        "display_inches": 6.8,
        "battery_mah": 5000,
        "camera_main_mp": 108,
        "price_usd": 999
    }
]

question = "Compare Samsung Galaxy S23 Ultra and S22 Ultra for photography."

answer = generate_answer(question, sample_rows)

print("\n🔹 LLM Answer:\n")
print(answer)
