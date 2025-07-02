import json
from playwright.sync_api import sync_playwright

def is_junk(text):
    junk_phrases = [
        "©", "ISRO", "Govt. of INDIA", "Maintained by", "Best viewed",
        "Ver 3.0", "Last reviewed", "Served By:"
    ]
    return any(j.lower() in text.lower() for j in junk_phrases) or len(text.strip()) < 40

def clean_and_chunk(text):
    lines = text.split("\n")
    cleaned = [' '.join(line.strip().split()) for line in lines]
    return [line for line in cleaned if line and not is_junk(line)]

def scrape_page_raw_text(url, label):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        full_text = page.locator("body").inner_text()
        browser.close()

        chunks = clean_and_chunk(full_text)
        return [{"source": label, "text": chunk} for chunk in chunks]

def run_scraper():
    faq_data = scrape_page_raw_text("https://www.mosdac.gov.in/faq-page#n1276", "faq")
    sat_data = scrape_page_raw_text("https://www.mosdac.gov.in/catalog/satellite.php", "satellite-series")

    all_data = faq_data + sat_data

    with open("mosdac_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped and saved {len(all_data)} clean text chunks to mosdac_data.json")

if __name__ == "__main__":
    run_scraper()
