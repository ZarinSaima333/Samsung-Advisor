from database import get_connection

def insert_device(device):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO samsung_devices (
            model, series, device_type,
            release_date,
            display_inches, display_area_cm2, screen_body_ratio,
            battery_mah, battery_type,
            camera_main_mp,
            ram_options_gb, storage_options_gb,
            price_value, price_currency, price_usd,
            source_url
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        device["model"],
        device["series"],
        "phone",
        device["release_date"],
        device["display_inches"],
        device["display_area_cm2"],
        device["screen_body_ratio"],
        device["battery_mah"],
        device["battery_type"],
        device["camera_main_mp"],
        device["ram_options"],
        device["storage_options"],
        device["price_value"],
        device["price_currency"],
        device["price_usd"],
        device["source_url"]
    ))

    conn.commit()
    cur.close()
    conn.close()
