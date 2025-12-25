import requests
import pdfplumber
import json
from config import DATA_FILE

PDF_URL = "https://www.poe.pl.ua/disconnection/hrafik-pohodynnoho-vidkliuchennia-elektroenerhii/grafik.pdf"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TelegramBot/1.0)"
}

def download_pdf():
    try:
        r = requests.get(
            PDF_URL,
            headers=HEADERS,
            timeout=15  # ⬅️ КРИТИЧНО
        )
        r.raise_for_status()

        with open("grafik.pdf", "wb") as f:
            f.write(r.content)

        return "grafik.pdf"

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка загрузки PDF: {e}")
        return None


def parse_pdf(file_path):
    if not file_path:
        return []

    data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                data.extend(text.split("\n"))

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return data


def update_schedule():
    pdf = download_pdf()
    return parse_pdf(pdf)