from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

URLS = [
    "https://www.abplive.com/",
    "https://news.abplive.com/"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for url in URLS:
        try:
            page = browser.new_page(viewport={"width": 1366, "height": 768})

            # Load page
            page.goto(url, timeout=60000)
            page.wait_for_timeout(8000)

            # IST Time
            now_utc = datetime.utcnow()
            now_ist = now_utc + timedelta(hours=5, minutes=30)

            time_text = now_ist.strftime("%H:%M")
            date_text = now_ist.strftime("%d-%b-%Y")

            # File name
            site_name = url.replace("https://", "").replace("www.", "").replace("/", "")
            filename = f"{site_name}_{now_ist.strftime('%Y-%m-%d_%H-%M-%S')}.png"

            # Screenshot
            page.screenshot(path=filename)

            # 🔥 Add full bottom taskbar strip
            img = Image.open(filename)
            draw = ImageDraw.Draw(img)

            width, height = img.size
            strip_height = 80

            # Black strip
            draw.rectangle((0, height - strip_height, width, height), fill="black")

            # Fonts (default)
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

            # Position (right side like Windows)
            x_time = width - 150
            y_time = height - 65

            x_date = width - 150
            y_date = height - 35

            # Draw text
            draw.text((x_time, y_time), time_text, fill="white", font=font_large)
            draw.text((x_date, y_date), date_text, fill="white", font=font_small)

            # Save image
            img.save(filename)

            print("✅ Saved:", filename)

            page.close()

        except Exception as e:
            print("❌ Error:", url, e)

    browser.close()
