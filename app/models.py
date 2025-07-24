import sqlite3

conn = sqlite3.connect("results.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    session TEXT PRIMARY KEY,
    type TEXT,
    status TEXT,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

def save_task(session_id: str, option: str, status: str = "pending", result: str = ""):
    cursor.execute("REPLACE INTO tasks (session, type, status, result) VALUES (?, ?, ?, ?)",
                   (session_id, option, status, result))
    conn.commit()

def update_result(session_id: str, result: str):
    cursor.execute("UPDATE tasks SET status = 'done', result = ? WHERE session = ?", (result, session_id))
    conn.commit()

def fetch_result(session_id: str):
    cursor.execute("SELECT status, result FROM tasks WHERE session = ?", (session_id,))
    return cursor.fetchone()