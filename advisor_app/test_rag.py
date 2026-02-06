# test_rag.py
from database import SessionLocal
from rag import generate_sql_and_fetch

def test_rag():
    db = SessionLocal()
    try:
        question = "Show me the phones with display larger than 6.5 inches."
        rows = generate_sql_and_fetch(question, db)
        print("Fetched rows:", rows)

        question2 = "What is the latest samsung phone?"
        rows2 = generate_sql_and_fetch(question2, db)
        print("Fetched rows:", rows2)

    finally:
        db.close()

if __name__ == "__main__":
    test_rag()
