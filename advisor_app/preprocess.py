import re
from datetime import datetime

USD_TO_USD = 1.0
EUR_TO_USD = 1.08
INR_TO_USD = 0.012

def extract_number(text):
    if not text:
        return None
    match = re.findall(r"[\d.]+", text)
    return float(match[0]) if match else None


def normalize_price(price_text):
    if not price_text:
        return None, None, None

    value = extract_number(price_text)

    if "$" in price_text:
        return value, "USD", value * USD_TO_USD
    elif "€" in price_text:
        return value, "EUR", value * EUR_TO_USD
    elif "₹" in price_text:
        return value, "INR", value * INR_TO_USD
    else:
        return value, "UNKNOWN", None


def parse_release_date(text):
    try:
        return datetime.strptime(text, "%Y, %B %d").date()
    except:
        return None


def parse_series(model):
    if "Galaxy S" in model:
        return "S"
    if "Galaxy A" in model:
        return "A"
    if "Galaxy Z" in model:
        return "Z"
    if "Galaxy M" in model:
        return "M"
    return "Other"
