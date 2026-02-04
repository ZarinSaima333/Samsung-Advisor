import requests
from bs4 import BeautifulSoup
import time

def get_specs(soup):
    specs = {}
    rows = soup.select("table tr")
    for row in rows:
        label = row.select_one("td.ttl")
        value = row.select_one("td.nfo")
        if label and value:
            specs[label.text.strip()] = value.text.strip()
    return specs

def get_price_from_bd_site(url):
    # Try scraping price from a Bangladesh price listing page
    try:
        res = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(res.text, "html.parser")
        # example price selector — adapt if needed
        price_text = soup.find(text=lambda t: "৳" in t or "৳" in t)
        if price_text:
            return price_text.strip()
    except Exception as e:
        return "Price not found"
    return "Price not found"

gsmarena_urls = [
    "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12002.php",
    "https://www.gsmarena.com/samsung_galaxy_s22_ultra-11251.php",
    "https://www.gsmarena.com/samsung_galaxy_s23-12082.php"
]

# Example price pages for Bangladesh
price_pages = [
    "https://www.gsmarena.com.bd/samsung-galaxy-s23-ultra-5g/",  # price for S23 Ultra
    "https://www.gsmarena.com.bd/samsung-galaxy-s22-ultra-5g/",
    "https://www.gsmarena.com.bd/samsung-galaxy-s23-5g/"
]

for phone_url, price_url in zip(gsmarena_urls, price_pages):
    print("=" * 60)
    print(f"Scraping specs: {phone_url}")

    response = requests.get(
        phone_url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    )
    soup = BeautifulSoup(response.text, "html.parser")

    # Model name
    model_tag = soup.select_one("h1.specs-phone-name-title")
    model_name = model_tag.text.strip() if model_tag else "Unknown Model"

    specs = get_specs(soup)
    price = get_price_from_bd_site(price_url)

    print(f"📱 Model   : {model_name}")
    print(f"📅 Release : {specs.get('Announced', 'N/A')}")
    print(f"🖥 Display : {specs.get('Size', 'N/A')}")
    print(f"🔋 Battery : {specs.get('Type', 'N/A')}")
    print(f"📷 Camera : {specs.get('Single', specs.get('Triple', specs.get('Quad', 'N/A')))}")
    print(f"💾 Memory : {specs.get('Internal', 'N/A')}")
    print(f"💰 Price  : {price}")

    time.sleep(2)

print("\nDone!")
