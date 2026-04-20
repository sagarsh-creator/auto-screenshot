from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

URLS = [
    "https://www.abplive.com/",
    "https://news.abplive.com/"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for url in URLS:
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        # Load website
        page.goto(url, timeout=60000)
        page.wait_for_timeout(6000)

        # IST Time
        now_utc = datetime.utcnow()
        now_ist = now_utc + timedelta(hours=5, minutes=30)

        time_text = now_ist.strftime("%H:%M")
        date_text = now_ist.strftime("%d-%b-%Y")

        # 🔥 Inject REAL taskbar (HTML + CSS)
        page.evaluate(f"""
        let bar = document.createElement('div');
        bar.style.position = 'fixed';
        bar.style.bottom = '0';
        bar.style.left = '0';
        bar.style.width = '100%';
        bar.style.height = '48px';
        bar.style.background = 'rgba(32,32,32,0.9)';
        bar.style.display = 'flex';
        bar.style.justifyContent = 'flex-end';
        bar.style.alignItems = 'center';
        bar.style.fontFamily = 'Segoe UI, Arial';
        bar.style.color = 'white';
        bar.style.fontSize = '16px';
        bar.style.paddingRight = '20px';
        bar.style.zIndex = '999999';

        let time = document.createElement('div');
        time.innerHTML = "{time_text}<br><span style='font-size:12px;color:#ccc'>{date_text}</span>";

        bar.appendChild(time);
        document.body.appendChild(bar);
        """)

        # File name
        site_name = url.replace("https://", "").replace("www.", "").replace("/", "")
        filename = f"{site_name}_{now_ist.strftime('%Y-%m-%d_%H-%M-%S')}.png"

        # Screenshot
        page.screenshot(path=filename)

        print("Saved:", filename)

        page.close()

    browser.close()
