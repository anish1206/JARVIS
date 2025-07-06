import os
import json
import fitz  # PyMuPDF

PDF_DIR = "pdfs"
OUTPUT_JSON = "mosdac_data.json"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_blocks = []
    for page in doc:
        text = page.get_text().strip()
        paragraphs = [para.strip() for para in text.split('\n') if len(para.strip()) > 50]
        text_blocks.extend(paragraphs)
    return text_blocks

def main():
    if not os.path.exists(PDF_DIR):
        print("❌ No 'pdfs' directory found.")
        return

    all_data = []

    # Load existing scraped data (from HTML)
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            all_data = json.load(f)

    # Read and extract from each PDF
    for filename in os.listdir(PDF_DIR):
        if not filename.endswith(".pdf"):
            continue
        filepath = os.path.join(PDF_DIR, filename)
        print(f"📄 Extracting: {filename}")
        try:
            paragraphs = extract_text_from_pdf(filepath)
            for para in paragraphs:
                all_data.append({
                    "source": f"pdf-{filename}",
                    "text": para
                })
        except Exception as e:
            print(f"⚠️ Could not extract from {filename}: {e}")

    # Save combined data
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! PDF content added to {OUTPUT_JSON}. Total chunks: {len(all_data)}")

if __name__ == "__main__":
    main()
