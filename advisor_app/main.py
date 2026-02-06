# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from model import SamsungDevice

app = FastAPI(title="Samsung Phone Advisor")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "FastAPI is running!"}


# Test DB endpoint: fetch first 5 devices
@app.get("/test-db")
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
