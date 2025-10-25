import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.jumia.com.ng"

def get_category_products(category_url, max_pages=1):
    headers = {"User-Agent": "Mozilla/5.0"}
    products = []

    for page in range(1, max_pages + 1):
        url = f"{category_url}?page={page}#catalog-listing"
        print(f"Scraping: {url}")
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        for card in soup.select("article.prd a.core"):
            product = {}

            # URL
            href = card.get("href")
            product["url"] = BASE_URL + href if href else None

            # Title
            name_tag = card.select_one("div.name")
            product["title"] = name_tag.get_text(strip=True) if name_tag else None

            # Current price
            price_tag = card.select_one("div.prc")
            product["price"] = price_tag.get_text(strip=True) if price_tag else None

            # Old price (from attribute)
            product["old_price"] = price_tag["data-oprc"] if price_tag and price_tag.has_attr("data-oprc") else None

            # Discount
            discount_tag = card.select_one("div.bdg._dsct")
            product["discount"] = discount_tag.get_text(strip=True) if discount_tag else None

            products.append(product)

        time.sleep(2)  # polite delay

    return products

if __name__ == "__main__":
    category_url = "https://www.jumia.com.ng/phones-tablets/"
    results = get_category_products(category_url, max_pages=1)
    print(f"Found {len(results)} products")
    for r in results[:5]:
        print(r)
