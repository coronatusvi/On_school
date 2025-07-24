from .models import update_result
import requests
from bs4 import BeautifulSoup
import asyncio
import sys
from playwright.async_api import async_playwright

# Simulate heavy CPU task

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def calculate_heavy(session_id: str):
    try:
        total = 1
        for i in range(1, 500):
            total *= i*i*i
        result = str(total ** 2)[:1000]
        html = f"<html><body><h2>Calculation Result</h2><p>Result: {result}</p></body></html>"
        update_result(session_id, html)
    except Exception as e:
        update_result(session_id, f"<html><body><p>Error: {e}</p></body></html>")

# Crawl Skyscanner (for demo purpose only)

def crawl_flights_with_playwright(session_id: str):
    """
    Crawl vocabulary table from a learning website and save as HTML result.
    """
    async def run():
        try:
            url = "https://chungchitienganhtinhoc.net/tu-vung-tieng-anh-b1/"
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(3000)  # wait for content to load (HTML is static)

                # Get full DOM after load
                content = await page.evaluate("document.documentElement.innerHTML")
                await browser.close()

                soup = BeautifulSoup(content, "html.parser")
                tables = soup.find_all("table")

                if not tables:
                    raise ValueError("Không tìm thấy bảng từ vựng!")

                # Parse all tables, make a nice HTML
                html_result = "<html><body><h2>Vocabulary Tables</h2>"
                for idx, table in enumerate(tables):
                    html_result += f"<h3>Bảng {idx + 1}</h3>"
                    html_result += str(table)

                html_result += "</body></html>"

                update_result(session_id, html_result)

        except Exception as e:
            update_result(session_id, f"<html><body><p>Error: {e}</p></body></html>")

    asyncio.run(run())

def crawl_flights_with_requests(session_id: str):
    try:
        url = "https://www.skyscanner.com.vn/flights/den-khoi-hanh/hnd/tokyo-haneda-den-khoi-hanh"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        flights = soup.select("section.FlightEntry_FlightEntry__MThhO")

        table_html = "<h2>Thông tin chuyến bay</h2><table border='1'>"
        table_html += "<tr><th>Hãng</th><th>Số hiệu</th><th>Giờ</th><th>Nơi đến</th><th>Trạng thái</th><th>Ga & Cổng</th></tr>"

        for f in flights:
            try:
                airline = f.select_one("div.FlightEntry_FlightEntry__airline__M2IyZ").text.strip()
                flight_code = f.select_one("div.FlightEntry_FlightEntry__flightCode__Y2I2Y").text.strip()
                time = f.select_one("div.FlightEntry_FlightEntry__time__YTQ5N").text.strip()
                location = f.select_one("div.FlightEntry_FlightEntry__location__ODcxN").text.strip()
                status = f.select_one("div.FlightEntry_FlightEntry__status__OGEwM").text.strip()
                terminal = f.select_one("div.FlightEntry_FlightEntry__terminal__ZDc5Z").text.strip()
                gate = f.select_one("div.FlightEntry_FlightEntry__gate__Y2ZhM").text.strip()

                table_html += f"<tr><td>{airline}</td><td>{flight_code}</td><td>{time}</td><td>{location}</td><td>{status}</td><td>{terminal}, {gate}</td></tr>"
            except:
                continue  # bỏ qua nếu một flight nào đó thiếu thông tin

        table_html += "</table>"
        html = f"<html><body>{table_html}</body></html>"

        update_result(session_id, html)

    except Exception as e:
        update_result(session_id, f"<html><body><p>Error: {e}</p></body></html>")

