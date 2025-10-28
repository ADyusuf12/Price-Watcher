from bs4 import BeautifulSoup
import requests
import re

def scrape_product(url_or_file, from_file=False):
    if from_file:
        with open(url_or_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")
    else:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url_or_file, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

    # Product title
    title_tag = soup.find("h1", class_="-fs20 -pts -pbxs")
    title = " ".join(title_tag.stripped_strings) if title_tag else "Unknown"

    # Current price
    price_tag = soup.find("span", class_="-b -ubpt -tal -fs24 -prxs")
    price = " ".join(price_tag.stripped_strings) if price_tag else "Unknown"

    # Old price
    old_price_tag = soup.find("span", class_="-tal -gy5 -lthr -fs16 -pvxs -ubpt")
    old_price = " ".join(old_price_tag.stripped_strings) if old_price_tag else None

    # Normalize whitespace
    def clean_text(text):
        return re.sub(r"\s+", " ", text).strip() if text else None

    return {
        "title": clean_text(title),
        "price": clean_text(price),
        "old_price": clean_text(old_price)
    }

if __name__ == "__main__":
    # Example: scrape from a saved file
    # result = scrape_product("jumia_product.html", from_file=True)
    # print(result)

    # Example: scrape live from URL
    url = "https://www.jumia.com.ng/xiaomi-redmi-note-14-6.67-8gb-ram256-gb-rom-hyperos-108mp-ai-camera-midnight-black-401065205.html"
    print(scrape_product(url))
