import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.who.int"
FACTSHEET_URL = "https://www.who.int/news-room/fact-sheets"
OUTPUT_FILE = "who_disease_links.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_all_disease_links():
    try:
        resp = requests.get(FACTSHEET_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Unable to load fact sheets page: {e}")
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")
    disease_links = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/news-room/fact-sheets/detail/" in href:
            title = a.get_text(strip=True)
            if not title:
                continue
            full_url = href if href.startswith("http") else BASE_URL + href
            # Build a clean key for filename use:
            key = href.rstrip("/").split("/")[-1]
            disease_links[key] = full_url

    print(f"[INFO] Found {len(disease_links)} links.")
    os.makedirs("separated jsons", exist_ok=True)
    with open(os.path.join("separated jsons", OUTPUT_FILE), "w", encoding="utf-8") as f:
        json.dump(disease_links, f, indent=2, ensure_ascii=False)

    return disease_links

if __name__ == "__main__":
    get_all_disease_links()
