# routes.py
from fastapi import APIRouter, Depends
from model import SamsungDevice
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from rag import generate_sql_and_fetch
from llm import generate_answer

router = APIRouter()
class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(req: QuestionRequest, db: Session = Depends(get_db)):
    # Step 1: RAG -> generate SQL + fetch rows
    db_rows = generate_sql_and_fetch(req.question, db)
    
    # Step 2: LLM -> generate natural language answer
    answer = generate_answer(req.question, db_rows)
    
    return {"answer": answer}

# Health check
@router.get("/health")
def health_check():
    return {"status": "OK", "message": "FastAPI is running!"}


# Test DB endpoint: fetch first 5 devices
@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    devices = db.query(SamsungDevice).limit(5).all()
    if not devices:
        return {"status": "DB connected", "devices": [], "message": "No devices found"}
    
    result = []
    for device in devices:
        result.append({
            "model": device.model,
            "release_date": str(device.release_date),
            "price_usd": device.price_usd
        })
    return {"status": "DB connected", "devices": result}

