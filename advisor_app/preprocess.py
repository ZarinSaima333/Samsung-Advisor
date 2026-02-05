# preprocess.py
import re
from datetime import datetime

def extract_number(text):
    if not text:
        return None
    match = re.findall(r"[\d\.]+", text.replace(",", ""))
    return float(match[0]) if match else None

def normalize_price(price_text):
    if not price_text:
        return None, None, None
    # Example: "About 150 EUR"
    match = re.search(r"([\d\.]+)\s*([A-Z]{2,3})", price_text)
    if not match:
        return None, None, None
    value, currency = match.groups()
    value = float(value)

    # convert to USD (example rates)
    rates = {"EUR": 1.1, "INR": 0.012, "USD": 1}
    usd = value * rates.get(currency, 1)
    return value, currency, round(usd, 2)

def parse_release_date(text):
    if not text:
        return None
    # Example: "2026, January 13"
    try:
        return datetime.strptime(text.strip(), "%Y, %B %d").date()
    except:
        return None

def parse_series(model_name):
    if not model_name:
        return "Other"
    model_name = model_name.upper()
    if model_name.startswith("GALAXY A"):
        return "A"
    elif model_name.startswith("GALAXY M"):
        return "M"
    elif model_name.startswith("GALAXY S"):
        return "S"
    elif model_name.startswith("GALAXY Z"):
        return "Z"
    else:
        return "Other"
