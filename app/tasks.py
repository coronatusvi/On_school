from .models import update_result
import requests
from bs4 import BeautifulSoup

# Simulate heavy CPU task

def calculate_heavy(session_id: str):
    try:
        total = 1
        for i in range(1, 500):
            total *= i
        result = str(total ** 2)[:1000]
        html = f"<html><body><h2>Calculation Result</h2><p>Result: {result}</p></body></html>"
        update_result(session_id, html)
    except Exception as e:
        update_result(session_id, f"<html><body><p>Error: {e}</p></body></html>")

# Crawl Skyscanner (for demo purpose only)

def crawl_flights(session_id: str):
    try:
        url = "https://www.skyscanner.com.vn/flights/den-khoi-hanh/hnd/tokyo-haneda-den-khoi-hanh"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table_html = "<h2>Flight Info</h2><table border='1'><tr><th>Example</th></tr>"
        for i in range(5):
            table_html += f"<tr><td>Flight Info {i+1} (placeholder)</td></tr>"
        table_html += "</table>"
        html = f"<html><body>{table_html}</body></html>"
        update_result(session_id, html)
    except Exception as e:
        update_result(session_id, f"<html><body><p>Error: {e}</p></body></html>")