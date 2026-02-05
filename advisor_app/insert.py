# insert.py
from database import get_connection

def insert_device(device):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    INSERT INTO samsung_devices (
        model, series, device_type, release_date, display_inches,
        display_area_cm2, screen_body_ratio, battery_mah, battery_type,
        camera_main_mp, ram_options_gb, storage_options_gb,
        price_value, price_currency, price_usd, source_url
    ) VALUES (
        %(model)s, %(series)s, 'phone', %(release_date)s, %(display_inches)s,
        %(display_area_cm2)s, %(screen_body_ratio)s, %(battery_mah)s, %(battery_type)s,
        %(camera_main_mp)s, %(ram_options)s, %(storage_options)s,
        %(price_value)s, %(price_currency)s, %(price_usd)s, %(source_url)s
    )
    """
    cur.execute(query, device)
    conn.commit()
    cur.close()
    conn.close()
