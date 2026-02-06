import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://www.gsmarena.com/"
LIST_URL = "https://www.gsmarena.com/samsung-phones-9.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def get_soup(url, retries=5):
    """Get BeautifulSoup object with retry logic"""
    for i in range(retries):
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            if res.status_code == 200 and "Too Many Requests" not in res.text:
                return BeautifulSoup(res.text, "html.parser")
            wait = random.uniform(5, 10)
            print(f"⚠️ Blocked! Retry {i+1} after {wait:.1f}s")
            time.sleep(wait)
        except Exception as e:
            print(f"⚠️ Request error: {e}")
            time.sleep(wait)
    raise Exception("❌ Could not fetch page, too many requests")

def get_phone_links():
    """Get all Samsung phone links from GSMArena"""
    soup = get_soup(LIST_URL)
    phone_links = []
    for phone in soup.select(".makers li a"):
        href = phone.get("href")
        if href:
            phone_links.append(BASE_URL + href)
    return phone_links

def get_phone_specs(url):
    """Extract full specifications from a phone page"""
    soup = get_soup(url)
    
    # Model name
    model = soup.find("h1").text.strip()
    
    specs = {}
    for row in soup.select("table tr"):
        label = row.select_one("td.ttl")
        value = row.select_one("td.nfo")
        if label and value:
            specs[label.text.strip()] = value.text.strip()
    
    # Map fields
    release_date = specs.get("Announced")
    display = specs.get("Size")
    display_area = specs.get("Display area")
    screen_ratio = specs.get("Screen-to-body ratio")
    battery = specs.get("Battery")
    battery_type = specs.get("Type")
    camera = specs.get("Single", specs.get("Dual", specs.get("Triple")))
    memory = specs.get("Internal")
    price = specs.get("Price")
    
    return {
        "model": model,
        "release": release_date,
        "display": display,
        "display_area": display_area,
        "screen_ratio": screen_ratio,
        "battery": battery,
        "battery_type": battery_type,
        "camera": camera,
        "memory": memory,
        "price": price,
        "source_url": url
    }

# Test function
if __name__ == "__main__":
    links = get_phone_links()
    print(f"🔍 Found {len(links)} Samsung devices")

