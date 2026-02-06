# model.py
from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class SamsungDevice(Base):
    __tablename__ = "samsung_devices"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    series = Column(String)
    device_type = Column(String, default="phone")
    release_date = Column(Date)
    display_inches = Column(Float)
    battery_mah = Column(Integer)
    battery_type = Column(String)
    camera_main_mp = Column(Float)
    price_value = Column(Float)
    price_currency = Column(String)
    price_usd = Column(Float)
    source_url = Column(String)
    price_bdt = Column(Float)
    storage = Column(String)