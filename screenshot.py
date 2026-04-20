from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

URLS = [
    "https://www.abplive.com/",
    "https://news.abplive.com/"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for url in URLS:
        try:
            page = browser.new_page(viewport={"width": 1366, "height": 768})

            page.goto(url, timeout=60000)
            page.wait_for_timeout(8000)

            now_utc = datetime.utcnow()
            now_ist = now_utc + timedelta(hours=5, minutes=30)
            time_text = now_ist.strftime("%Y-%m-%d %H:%M:%S")

            site_name = url.replace("https://", "").replace("www.", "").replace("/", "")
            filename = f"{site_name}_{now_ist.strftime('%Y-%m-%d_%H-%M-%S')}.png"

            page.screenshot(path=filename)

            img = Image.open(filename)
            draw = ImageDraw.Draw(img)
            draw.rectangle((20, 20, 600, 80), fill="black")
            draw.text((30, 30), f"Time: {time_text}", fill="white")
            img.save(filename)

            print("Saved:", filename)

            page.close()

        except Exception as e:
            print("Error:", url, e)

    browser.close()
