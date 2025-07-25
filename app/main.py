from fastapi import FastAPI, BackgroundTasks, Query, HTTPException
from fastapi.responses import HTMLResponse
from uuid import uuid4
from .models import save_task, fetch_result
from .tasks import calculate_heavy, crawl_flights_with_playwright
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import save_task, fetch_result

from .database import engine
from .models import Task
Task.metadata.create_all(bind=engine)


app = FastAPI(title="Async Task API Demo")

@app.get("/submit")
def submit(option: str = Query(..., regex="^(cal|crawl)$"), background_tasks: BackgroundTasks = None, db: Session = Depends(get_db)):
    session_id = str(uuid4())
    save_task(db, session_id, option)
    if option == "cal":
        background_tasks.add_task(calculate_heavy, session_id)
    elif option == "crawl":
        background_tasks.add_task(crawl_flights_with_playwright, session_id)
    return {"session": session_id, "status": "started"}

@app.get("/result/{session_id}", response_class=HTMLResponse)
def get_result(session_id: str, db: Session = Depends(get_db)):
    task = fetch_result(db, session_id)
    if task is None:
        return HTMLResponse(content="<html><body><p>Status: not found</p></body></html>", status_code=404)

    status = getattr(task, "status", None)
    result = getattr(task, "result", None)
    duration = getattr(task, "duration", None)

    if status != "done":
        return HTMLResponse(content=f"<html><body><p>Status: {status}</p></body></html>", status_code=202)

    extra = f"<p><b>⏱️ Time taken:</b> {duration:.2f} seconds</p>" if duration else ""
    return HTMLResponse(content=(result or "") + extra, status_code=200)