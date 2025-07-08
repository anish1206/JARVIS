import os
import re
import json
import requests
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.mosdac.gov.in"
OUTPUT_JSON = "mosdac_data.json"
PDF_DIR = "pdfs"
MAX_PAGES = 100  # Change this to increase/decrease page depth

os.makedirs(PDF_DIR, exist_ok=True)

def is_junk(text):
    return (
        len(text.strip()) < 40 or
        re.match(r'^\W*$', text.strip()) or
        any(j in text.lower() for j in [
            "govt. of india", "best viewed", "isro", "privacy policy", "copyright"
        ])
    )

def group_paragraphs(lines, max_len=500):
    chunks = []
    buffer = ""
    for line in lines:
        line = line.strip()
        if not line or is_junk(line):
            continue
        buffer += " " + line
        if len(buffer) >= max_len or line.endswith(('.', ':', ';')):
            chunks.append(buffer.strip())
            buffer = ""
    if buffer:
        chunks.append(buffer.strip())
    return chunks

def download_pdf(pdf_url):
    try:
        filename = os.path.basename(urlparse(pdf_url).path)
        filepath = os.path.join(PDF_DIR, filename)
        if not os.path.exists(filepath):
            print(f"⬇️ Downloading PDF: {filename}")
            r = requests.get(pdf_url, timeout=15)
            with open(filepath, "wb") as f:
                f.write(r.content)
    except Exception as e:
        print(f"⚠️ Failed to download PDF: {pdf_url} — {e}")

def get_internal_links_and_pdfs(page):
    internal_links = set()
    pdf_links = set()
    anchors = page.locator("a").all()
    for a in anchors:
        try:
            href = a.get_attribute("href")
            if not href:
                continue
            href = href.strip()
            full_url = urljoin(BASE_URL, href.split("#")[0])
            if href.endswith(".pdf"):
                pdf_links.add(full_url)
            elif BASE_URL in full_url or href.startswith("/"):
                if "login" not in full_url and "dataaccess" not in full_url:
                    internal_links.add(full_url)
        except:
            continue
    return internal_links, pdf_links

def scrape_all_mosdac():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        visited = set()
        to_visit = {BASE_URL}
        all_chunks = []

        while to_visit:
            url = to_visit.pop()
            if url in visited or len(visited) >= MAX_PAGES:
                continue

            print(f"🌐 Visiting: {url}")
            try:
                page.goto(url, timeout=15000)
                page.wait_for_load_state("domcontentloaded", timeout=10000)
            except:
                print(f"⏳ Skipping slow page: {url}")
                continue

            visited.add(url)

            try:
                text = page.locator("body").inner_text()
                lines = text.splitlines()
                chunks = group_paragraphs(lines)
                slug = urlparse(url).path.strip("/").replace("/", "-") or "home"
                for chunk in chunks:
                    all_chunks.append({
                        "source": slug,
                        "text": chunk
                    })

                new_links, pdf_links = get_internal_links_and_pdfs(page)
                to_visit.update(new_links - visited)

                for pdf_url in pdf_links:
                    download_pdf(pdf_url)

            except Exception as e:
                print(f"⚠️ Error scraping {url}: {e}")
                continue

        browser.close()
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Done! {len(visited)} pages visited, {len(all_chunks)} chunks saved.")

if __name__ == "__main__":
    scrape_all_mosdac()
