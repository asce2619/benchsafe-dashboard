import sqlite3
import time
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_engine import generate_ai_report

app = FastAPI(title="BENCHSAFE Integration Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SQLite Database Setup ---
DB_NAME = "benchsafe.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            detail TEXT NOT NULL,
            report TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    # Insert default mock entries if empty
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        default_events = [
            ("2026-11-05 14:32:01", "SENSOR", "High Temp (>50°C)", "Temp spike detected. Local cutoff activated at 2026-11-05 14:32:01."),
            ("2026-11-05 14:30:12", "VISION", "Missing Safety Glasses", "Unsafe visual condition flagged at 2026-11-05 14:30:12.")
        ]
        cursor.executemany("INSERT INTO events (timestamp, source, detail, report) VALUES (?, ?, ?, ?)", default_events)
        conn.commit()
        
    conn.close()

init_db()

class IncomingEventPayload(BaseModel):
    source: str         # "SENSOR" or "VISION"
    detail: str         # e.g., "High Temp (>50°C)", "Missing Safety Glasses", "Tool Near Edge"
    cutoff_active: Optional[bool] = False

@app.get("/api/logs")
def get_logs():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, source, detail, report FROM events ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    events = [dict(row) for row in rows]
    return {"events": events}

@app.post("/api/events")
def receive_event(payload: IncomingEventPayload):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    ai_summary = generate_ai_report(
        timestamp=timestamp,
        source=payload.source,
        detail=payload.detail,
        cutoff_active=payload.cutoff_active
    )
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (timestamp, source, detail, report) VALUES (?, ?, ?, ?)",
        (timestamp, payload.source.upper(), payload.detail, ai_summary)
    )
    conn.commit()
    conn.close()
    
    new_event = {
        "timestamp": timestamp,
        "source": payload.source.upper(),
        "detail": payload.detail,
        "report": ai_summary
    }
    
    print(f"[SAVED TO DATABASE & LOGGED] {new_event}")
    return {"status": "success", "event": new_event}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)