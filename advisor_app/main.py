import time
from scraper import get_phone_links, scrape_phone
from preprocess import (
    extract_number,
    normalize_price,
    parse_release_date,
    parse_series
)
from insert import insert_device

links = get_phone_links()
print(f"🔍 Found {len(links)} Samsung devices")

for url in links:
    try:
        raw = scrape_phone(url)

        price_value, price_currency, price_usd = normalize_price(raw["price"])

        device = {
            "model": raw["model"],
            "series": parse_series(raw["model"]),
            "release_date": parse_release_date(raw["release"]),
            "display_inches": extract_number(raw["display"]),
            "display_area_cm2": extract_number(raw["display_area"]),
            "screen_body_ratio": extract_number(raw["screen_ratio"]),
            "battery_mah": extract_number(raw["battery"]),
            "battery_type": raw["battery_type"],
            "camera_main_mp": extract_number(raw["camera"]),
            "ram_options": raw["memory"],
            "storage_options": raw["memory"],
            "price_value": price_value,
            "price_currency": price_currency,
            "price_usd": price_usd,
            "source_url": raw["source_url"]
        }

        insert_device(device)
        print(f"✅ Inserted: {device['model']}")

        time.sleep(1)

    except Exception as e:
        print(f"❌ Failed for {url}: {e}")
