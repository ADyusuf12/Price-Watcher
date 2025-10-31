import time
import os
import psycopg2
import requests
from datetime import datetime, UTC
from dotenv import load_dotenv
from jumia_category_scraper import get_category_products
from jumia_detail_scraper import scrape_product

# Load environment variables from .env at project root
load_dotenv()

CHECKPOINT_FILE = "jumia_checkpoint.txt"

# --- Safe request wrapper ---
def safe_get(url, headers=None, retries=3, backoff=5):
    for attempt in range(retries):
        try:
            return requests.get(url, headers=headers, timeout=15)
        except requests.exceptions.RequestException as e:
            print(f"Request failed ({e}), attempt {attempt+1}/{retries}")
            time.sleep(backoff * (attempt+1))
    return None

# --- Price normalization ---
def normalize_price(p):
    if not p or p == "Unknown":
        return None
    try:
        return int(p.replace("₦", "").replace(",", "").strip())
    except ValueError:
        return None

# --- Save one product immediately ---
def save_one_to_postgres(item):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (url, title, price, old_price, discount, scraped_at, image, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
    """, (
        item["url"],
        item["title"],
        item["price"],
        item["old_price"],
        item["discount"],
        item["scraped_at"],
        item["image"],
        item["source"]
    ))
    conn.commit()
    cur.close()
    conn.close()

# --- Main scrape loop with checkpointing ---
def scrape_category_with_details(category_url, max_pages=1):
    products = get_category_products(category_url, max_pages=max_pages)

    # Resume from checkpoint if exists
    start_index = 0
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            start_index = int(f.read().strip() or 0)

    print(f"Starting scrape at index {start_index}/{len(products)}")

    for i, product in enumerate(products[start_index:], start=start_index):
        print(f"\nScraping detail page {i+1}/{len(products)}: {product['url']}")

        details = scrape_product(product["url"])
        current_price = normalize_price(details.get("price"))
        old_price = normalize_price(details.get("old_price"))

        discount = None
        if current_price and old_price and old_price > current_price:
            percent = round((old_price - current_price) / old_price * 100)
            discount = f"{percent}%"

        merged = {
            **product,
            **details,
            "price": current_price,
            "old_price": old_price,
            "discount": discount,
            "scraped_at": datetime.now(UTC).isoformat(),
            "source": "jumia"
        }

        save_one_to_postgres(merged)

        # Update checkpoint
        with open(CHECKPOINT_FILE, "w") as f:
            f.write(str(i+1))

        time.sleep(2)  # be polite

    print("Scraping complete ✅")

if __name__ == "__main__":
    category_url = "https://www.jumia.com.ng/phones-tablets/"
    scrape_category_with_details(category_url, max_pages=3)
