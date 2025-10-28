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

        for card in soup.select("article.prd"):
            link_tag = card.select_one("a.core")
            href = link_tag.get("href") if link_tag else None
            title_tag = card.select_one("div.name")
            img_tag = card.select_one("img")

            image = None
            if img_tag:
                image = img_tag.get("data-src") or img_tag.get("src")

            product = {
                "url": BASE_URL + href if href else None,
                "title": title_tag.get_text(strip=True) if title_tag else None,
                "image": image
            }

            products.append(product)

        time.sleep(2)

    return products

if __name__ == "__main__":
    category_url = "https://www.jumia.com.ng/phones-tablets/"
    results = get_category_products(category_url, max_pages=1)
    print(f"Found {len(results)} products")
    for r in results[:5]:
        print(r)
