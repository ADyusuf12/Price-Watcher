import asyncio
import time
import os
import psycopg2
import requests
from datetime import datetime, UTC
from dotenv import load_dotenv
from konga_category_scraper import scrape_konga_category
from konga_detail_scraper import scrape_product_detail

# Load environment variables from .env
load_dotenv()

CHECKPOINT_FILE = "konga_checkpoint.txt"

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
async def run_pipeline(category_url, n_pages=3):
    category_products = await scrape_konga_category(category_url, n_pages=n_pages)

    # Resume from checkpoint if exists
    start_index = 0
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            start_index = int(f.read().strip() or 0)

    print(f"Starting scrape at index {start_index}/{len(category_products)}")

    for i, item in enumerate(category_products[start_index:], start=start_index):
        print(f"\n🔍 Scraping detail page {i+1}/{len(category_products)}: {item['url']}")
        detail = await scrape_product_detail(item["url"])

        if detail.get("title"):
            current_price = normalize_price(detail.get("current_price"))
            old_price = normalize_price(detail.get("old_price"))

            discount = None
            if current_price and old_price and old_price > current_price:
                percent = round((old_price - current_price) / old_price * 100)
                discount = f"{percent}%"

            merged = {
                **item,
                **detail,
                "price": current_price,
                "old_price": old_price,
                "discount": discount,
                "scraped_at": datetime.now(UTC).isoformat(),
                "source": "konga"
            }

            save_one_to_postgres(merged)
        else:
            print(f"⚠️ Skipping product due to missing detail: {item['url']}")

        # Update checkpoint
        with open(CHECKPOINT_FILE, "w") as f:
            f.write(str(i+1))

        time.sleep(2)

    print("✅ Scraping complete")

if __name__ == "__main__":
    category_url = "https://www.konga.com/category/phones-tablets-5294"
    asyncio.run(run_pipeline(category_url, n_pages=3))
