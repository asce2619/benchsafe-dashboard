import sqlite3

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

def get_all_events():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, source, detail, report FROM events ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_event(timestamp, source, detail, report):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (timestamp, source, detail, report) VALUES (?, ?, ?, ?)",
        (timestamp, source, detail, report)
    )
    conn.commit()
    conn.close()