import asyncio
import time
from datetime import datetime, UTC
from konga_category_scraper import scrape_konga_category
from konga_detail_scraper import scrape_product_detail
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def normalize_price(p):
    if not p:
        return None
    return int(p.replace("₦", "").replace(",", "").strip())

def save_to_postgres(data):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    for item in data:
        cur.execute("""
            INSERT INTO products (url, title, price, old_price, discount, scraped_at, image, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item["url"],
            item["title"],
            normalize_price(item["current_price"]),
            normalize_price(item["old_price"]),
            item["discount"],
            item["scraped_at"],
            item["image"],
            item["source"]
        ))

    conn.commit()
    cur.close()
    conn.close()

async def run_pipeline(category_url, n_pages=1, limit=10):
    category_products = await scrape_konga_category(category_url, n_pages=n_pages)

    results = []
    for i, item in enumerate(category_products[:limit]):
        print(f"\n🔍 Scraping detail page {i+1}/{len(category_products)}: {item['url']}")
        detail = await scrape_product_detail(item["url"])

        if detail.get("title"):
            merged = {
                **item,
                **detail,
                "scraped_at": datetime.now(UTC).isoformat(),
                "source": "konga"
            }
            results.append(merged)
        else:
            print(f"⚠️ Skipping product due to missing detail: {item['url']}")

        time.sleep(2)

    return results

if __name__ == "__main__":
    category_url = "https://www.konga.com/category/phones-tablets-5294"
    data = asyncio.run(run_pipeline(category_url, n_pages=1, limit=5))

    print("\n💾 Saving to Postgres")
    save_to_postgres(data)
    print("✅ Done")
