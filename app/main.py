from fastapi import FastAPI, BackgroundTasks, Query, HTTPException
from fastapi.responses import HTMLResponse
from uuid import uuid4
from .models import save_task, fetch_result
from .tasks import calculate_heavy, crawl_flights_with_playwright, crawl_flights_with_requests

app = FastAPI(title="Async Task API Demo")

@app.get("/submit")
def submit(option: str = Query(..., regex="^(cal|crawl)$"), background_tasks: BackgroundTasks = None):
    session_id = str(uuid4())
    save_task(session_id, option)
    if option == "cal":
        background_tasks.add_task(calculate_heavy, session_id)
    elif option == "crawl":
        background_tasks.add_task(crawl_flights_with_playwright, session_id)
    return {"session": session_id, "status": "started"}

@app.get("/result/{session_id}", response_class=HTMLResponse)
def get_result(session_id: str):
    row = fetch_result(session_id)
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    status, result = row
    if status != "done":
        return HTMLResponse(content=f"<html><body><p>Status: {status}</p></body></html>", status_code=202)
    return HTMLResponse(content=result, status_code=200)