import asyncio
from playwright.async_api import async_playwright

async def scrape_product_detail(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, timeout=60000)
        except Exception as e:
            print(f"❌ Failed to load page: {url}\nError: {e}")
            await browser.close()
            return {
                "title": None,
                "current_price": None,
                "old_price": None,
                "discount": None,
                "image": None,
                "url": url,
                "source": "konga",
                "error": str(e)
            }

        # Title
        title_el = await page.query_selector("h4.productDetail_productName__a53Mh")
        title = (await title_el.inner_text()).strip() if title_el else None

        # Prices
        current_price_el = await page.query_selector("div.priceBox_priceBoxPrice__i7paS")
        old_price_el = await page.query_selector("div.priceBox_priceBoxOriginalPrice__ESlQ0")
        discount_el = await page.query_selector("span.priceBox_youSave__K_x_E")

        current_price = (await current_price_el.inner_text()).strip() if current_price_el else None
        old_price = (await old_price_el.inner_text()).strip() if old_price_el else None
        discount = (await discount_el.inner_text()).strip() if discount_el else None

        # Image (from active carousel slide)
        image = None
        try:
            await page.wait_for_selector("div.carousel_carouselSlideActive__wY_PQ img.asset_imageContain__sD8jM", timeout=10000)
            img_el = await page.query_selector("div.carousel_carouselSlideActive__wY_PQ img.asset_imageContain__sD8jM")
            if img_el:
                srcset = await img_el.get_attribute("srcset")
                if srcset:
                    last_entry = srcset.split(",")[-1].strip()
                    partial_url = last_entry.rsplit(" ", 1)[0]
                    if partial_url.startswith("http"):
                        image = partial_url
                    else:
                        image = f"https://www-konga-com-res.cloudinary.com/image/upload/{partial_url}"
                else:
                    raw_src = await img_el.get_attribute("src")
                    if raw_src and raw_src.startswith("http"):
                        image = raw_src
                    elif raw_src:
                        image = f"https://www-konga-com-res.cloudinary.com/image/upload/{raw_src}"
        except Exception as e:
            print(f"⚠️ Image not found for: {url}")

        await browser.close()

        return {
            "title": title,
            "current_price": current_price,
            "old_price": old_price,
            "discount": discount,
            "image": image,
            "url": url,
            "source": "konga"
        }

if __name__ == "__main__":
    test_url = "https://www.konga.com/product/zte-zte-blade-a35-6-75-4gb-ram-64gb-rom-5000mah-black-6508365"
    result = asyncio.run(scrape_product_detail(test_url))
    print(result)
