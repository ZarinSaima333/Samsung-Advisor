# test_db.py
from database import SessionLocal
from model import SamsungDevice

db = SessionLocal()
try:
    devices = db.query(SamsungDevice).limit(5).all()
    if devices:
        print("✅ Database connection successful! Found these devices:")
        for device in devices:
            print(f"- {device.model}, Release: {device.release_date}, Price: {device.price_usd} USD")
    else:
        print("⚠️ Database connected, but no devices found in table.")
finally:
    db.close()
