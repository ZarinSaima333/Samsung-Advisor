import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gsmarena.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_phone_links():
    url = "https://www.gsmarena.com/samsung-phones-9.php"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for phone in soup.select(".makers li a"):
        links.append(BASE_URL + phone["href"])

    return links


def scrape_phone(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    def get_spec(key):
        tag = soup.find("td", {"data-spec": key})
        return tag.text.strip() if tag else None

    phone = {
        "model": soup.find("h1").text.strip(),
        "release": get_spec("released-hl"),
        "display": get_spec("displaysize"),
        "display_area": get_spec("displayarea"),
        "screen_ratio": get_spec("displayratio"),
        "battery": get_spec("batcapacity"),
        "battery_type": get_spec("battype"),
        "camera": get_spec("cam1modules"),
        "memory": get_spec("internalmemory"),
        "price": get_spec("price"),
        "source_url": url
    }

    return phone
