# preprocess_and_insert.py
import re
from datetime import datetime
import psycopg2
import pdfplumber

# -------------------------
# Helper Functions
# -------------------------
def extract_number(text):
    if not text:
        return None
    text = text.replace(",", "")
    match = re.search(r"[\d\.]+", text)
    return float(match.group()) if match else None

def parse_release_date(text):
    if not text:
        return None
    try:
        return datetime.strptime(text.strip(), "%Y, %B %d").date()
    except:
        return None

# Currency conversion rates
CURRENCY_USD_RATE = {
    "USD": 1,
    "$": 1,
    "EUR": 1.1,
    "INR": 0.012,
    "₹": 0.012,
    "£": 1.3
}

USD_TO_BDT = 122.0  # 1 USD = 122 BDT

def normalize_price(text):
    if not text:
        return None, None, None, None
    match = re.search(r"([\d\.,]+)\s*([A-Z$₹£]+)?", text.replace(",", ""))
    if match:
        value = float(match.group(1))
        currency = match.group(2) if match.group(2) else "USD"
        usd = value * CURRENCY_USD_RATE.get(currency, 1)
        bdt = usd * USD_TO_BDT
        return value, currency, round(usd, 2), round(bdt, 2)
    return None, None, None, None

def parse_series(model):
    if not model:
        return "Other"
    match = re.search(r"Galaxy\s+([A-Z])", model)
    return match.group(1) if match else "Other"

# -------------------------
# Database functions
# -------------------------
def connect_db():
    return psycopg2.connect(
        dbname="Samsung_Phones",
        user="postgres",
        password="roza",
        host="localhost",
        port="5432"
    )

def insert_devices(devices):
    conn = connect_db()
    cur = conn.cursor()
    query = """
    INSERT INTO samsung_devices (
        model, series, device_type, release_date, display_inches,
        battery_mah, battery_type, camera_main_mp, storage,
        price_value, price_currency, price_usd, price_bdt, source_url
    ) VALUES (
        %(model)s, %(series)s, 'phone', %(release_date)s, %(display_inches)s,
        %(battery_mah)s, %(battery_type)s, %(camera_main_mp)s, %(storage)s,
        %(price_value)s, %(price_currency)s, %(price_usd)s, %(price_bdt)s, %(source_url)s
    )
    """
    for device in devices:
        try:
            cur.execute(query, device)
            conn.commit()
            print(f"✅ Inserted: {device['model']}")
        except Exception as e:
            print(f"❌ Failed to insert {device.get('model')}: {e}")
            conn.rollback()

    cur.close()
    conn.close()

# -------------------------
# Read PDF and preprocess
# -------------------------
pdf_path = "/Users/zarinsaimaroza/Downloads/samsung_scraped.pdf"
all_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

phones = all_text.split("============================================================")

devices = []

for phone_text in phones:
    if not phone_text.strip():
        continue

    model = re.search(r"📱 Model\s*:\s*(.*)", phone_text)
    release = re.search(r"📅 Release\s*:\s*(.*)", phone_text)
    battery = re.search(r"🔋 Battery\s*:\s*(.*)", phone_text)
    camera = re.search(r"📷 Camera\s*:\s*(.*)", phone_text)
    memory = re.search(r"💾 Memory\s*:\s*(.*)", phone_text)
    price = re.search(r"💰 Price\s*:\s*(.*)", phone_text)
    url = re.search(r"Scraping:\s*(.*)", phone_text)

    # -------------------------
    # Only extract display inches
    # Extract only display inches
    display_inches = None
    for line in phone_text.split("\n"):
        if "Display" in line:  # no emoji needed, just the word
            # normalize spaces
            line = line.replace("\xa0", " ").strip()  # remove non-breaking spaces
            # find a number followed by "inch" or "inches"
            match = re.search(r"([\d\.]+)\s*inches?", line, re.IGNORECASE)
            if match:
                display_inches = float(match.group(1))
            break


    battery_mah = extract_number(battery.group(1)) if battery else None
    battery_type = battery.group(1).split()[0] if battery else None
    camera_mp = extract_number(camera.group(1)) if camera else None
    storage_text = memory.group(1).strip() if memory else None  # single storage column
    price_value, price_currency, price_usd, price_bdt = normalize_price(price.group(1)) if price else (None, None, None, None)
    release_date = parse_release_date(release.group(1)) if release else None
    series = parse_series(model.group(1)) if model else "Other"

    device = {
        "model": model.group(1).strip() if model else None,
        "series": series,
        "release_date": release_date,
        "display_inches": display_inches,
        "battery_mah": battery_mah,
        "battery_type": battery_type,
        "camera_main_mp": camera_mp,
        "storage": storage_text,
        "price_value": price_value,
        "price_currency": price_currency,
        "price_usd": price_usd,
        "price_bdt": price_bdt,
        "source_url": url.group(1).strip() if url else None
    }

    devices.append(device)

# -------------------------
# Insert all devices
# -------------------------
insert_devices(devices)
print("✅ All devices inserted successfully!")
