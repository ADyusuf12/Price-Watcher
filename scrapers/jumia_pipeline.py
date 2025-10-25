import time
from datetime import datetime
from jumia_category_scraper import get_category_products
from jumia_detail_scraper import scrape_product
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env at project root
load_dotenv()

def scrape_category_with_details(category_url, max_pages=1, limit=10):
    products = get_category_products(category_url, max_pages=max_pages)

    results = []
    for i, product in enumerate(products[:limit]):
        print(f"\nScraping detail page {i+1}/{len(products)}: {product['url']}")
        details = scrape_product(product["url"])

        merged = {
            **product,
            **details,
            "scraped_at": datetime.utcnow().isoformat()
        }
        results.append(merged)
        time.sleep(2)

    return results

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
        # Normalize prices into integers
        def normalize_price(p):
            if not p:
                return None
            return int(p.replace("₦", "").replace(",", "").strip())

        cur.execute("""
            INSERT INTO products (url, title, price, old_price, discount, scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item["url"],
            item["title"],
            normalize_price(item["price"]),
            normalize_price(item["old_price"]),
            item["discount"],
            item["scraped_at"]
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    category_url = "https://www.jumia.com.ng/phones-tablets/"
    data = scrape_category_with_details(category_url, max_pages=1, limit=5)

    print("\n=== Saving to Postgres ===")
    save_to_postgres(data)
    print("Done ✅")
