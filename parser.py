import requests
from bs4 import BeautifulSoup

URL = "https://www.poe.pl.ua/disconnection/power-outages/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (TelegramBot)"
}

def update_schedule():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Сайт недоступен: {e}")

    soup = BeautifulSoup(r.text, "html.parser")

    result = []

    # Заголовки / новости
    for block in soup.select("article, .item, .views-row"):
        title = block.find(["h1", "h2", "h3"])
        text = block.get_text("\n", strip=True)

        if text and len(text) > 50:
            if title:
                result.append(f"📌 {title.get_text(strip=True)}")
            result.append(text)
            result.append("")

    # fallback — просто текст страницы
    if not result:
        text = soup.get_text("\n", strip=True)
        result = text.split("\n")

    return result