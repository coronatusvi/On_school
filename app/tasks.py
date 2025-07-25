from .models import update_result
import asyncio
import sys
from time import time
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from .database import SessionLocal

sys.set_int_max_str_digits(10000)
# Simulate heavy CPU task

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def calculate_heavy(session_id: str):
    db = SessionLocal()
    try:
        total = 1
        for i in range(1, 100):  # giảm từ 500 xuống 100
            total *= i*i
        result = str(total ** 2)[:1000]  # giảm số mũ từ 8 xuống 2
        html = f"<html><body><h2>Calculation Result</h2><p>Result: {result}</p></body></html>"
        update_result(db, session_id, html)
    except Exception as e:
        error_html = f"<html><body><p>Error: {e}</p></body></html>"
        update_result(db, session_id, error_html)
    finally:
        db.close()

# Crawl Skyscanner (for demo purpose only)
def crawl_flights_with_playwright(session_id: str):
    url = 'https://tailieuhoctiengnhat.com/100-tu-vung-tieng-nhat-co-ban.html'
    """
    Crawl vocabulary table from a learning website and save as HTML result.
    """

    async def run():
        db = SessionLocal()
        start = time()
        try:

            # Khởi tạo browser
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(3000)  # đợi trang tải hoàn toàn

                # Lấy toàn bộ nội dung HTML sau khi trang đã load
                content = await page.evaluate("document.documentElement.innerHTML")
                await browser.close()

            # Phân tích nội dung HTML
            soup = BeautifulSoup(content, "html.parser")
            tables = soup.find_all("table")

            if not tables:
                raise ValueError("Không tìm thấy bảng từ vựng!")

            # Ghép tất cả bảng thành HTML đẹp
            html_result = "<html><body><h2>📘 Vocabulary Tables</h2>"
            for idx, table in enumerate(tables):
                html_result += f"<h3>Bảng {idx + 1}</h3>{str(table)}"
            html_result += "</body></html>"

            # Tính thời gian xử lý
            duration = round(time() - start, 2)

            # Ghi kết quả vào DB
            update_result(db, session_id, html_result, duration=duration)

        except Exception as e:
            error_html = f"<html><body><p>Error: {e}</p></body></html>"
            update_result(db, session_id, error_html)

        finally:
            db.close()

    # Chạy async function trong sync context
    asyncio.run(run())
