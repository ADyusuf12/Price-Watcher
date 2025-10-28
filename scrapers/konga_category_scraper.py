import asyncio
from playwright.async_api import async_playwright

async def scrape_konga_category(category_url, n_pages=1):
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i in range(1, n_pages + 1):
            url = f"{category_url}?page={i}"
            await page.goto(url, timeout=120000)
            await asyncio.sleep(3)
            await page.wait_for_selector("div.ListingCard_listingCardMetaContainer__HCXHt")

            cards = await page.query_selector_all("div.ListingCard_listingCardMetaContainer__HCXHt")

            for card in cards:
                title_el = await card.query_selector("h3.ListingCard_productTitle__9Kzxv")
                title = (await title_el.inner_text()).strip() if title_el else None

                link_el = await card.query_selector("a")
                link = await link_el.get_attribute("href") if link_el else None
                if link and not link.startswith("http"):
                    link = f"https://www.konga.com{link}"

                products.append({"title": title, "url": link})

            print(f"✅ Page {i} scraped, {len(cards)} products")

        await browser.close()
    return products

# Only runs if you call this file directly
if __name__ == "__main__":
    category_url = "https://www.konga.com/category/phones-tablets-5294"
    results = asyncio.run(scrape_konga_category(category_url, n_pages=1))
    print(results[:5])
