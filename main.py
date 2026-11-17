from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db, get_all_events, insert_event
from llm_engine import generate_ai_report

app = FastAPI(title="BENCHSAFE Backend")

# Enable CORS so your frontend or external partner scripts can talk smoothly to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database table on startup
init_db()

class EventPayload(BaseModel):
    source: str
    detail: str
    cutoff_active: bool

@app.get("/api/logs")
def get_logs():
    return {"events": get_all_events()}

@app.post("/api/events")
def post_event(payload: EventPayload):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate verified report via LLM engine
    report = generate_ai_report(timestamp, payload.source, payload.detail, payload.cutoff_active)
    
    # Save into SQLite database
    insert_event(timestamp, payload.source.upper(), payload.detail, report)
    
    return {"status": "success", "timestamp": timestamp, "report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)