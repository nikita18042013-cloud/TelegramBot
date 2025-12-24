import requests
import pdfplumber
import json
from config import PDF_URL, DATA_FILE

def download_pdf():
    # Если сайт напрямую даёт ссылку на PDF, указываем полный URL
    url = PDF_URL + "grafik.pdf"  # пример, нужно проверить реальный URL
    r = requests.get(url)
    with open("grafik.pdf", "wb") as f:
        f.write(r.content)
    return "grafik.pdf"

def parse_pdf(file_path="grafik.pdf"):
    all_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            for l in lines:
                all_data.append(l)
    # Сохраняем как JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False)
    return all_data

def update_schedule():
    pdf_path = download_pdf()
    return parse_pdf(pdf_path)