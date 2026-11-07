import json, os, sqlite3
from pathlib import Path
from .config import DATABASE_URL
from .seed import seed_state

def _db_path():
    if DATABASE_URL.startswith("sqlite:///"):
        raw = DATABASE_URL.replace("sqlite:///", "", 1)
        path = Path(raw)
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[1] / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)
    raise RuntimeError("This demo build currently supports SQLite only.")

DB_PATH = _db_path()

def connect():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        row = db.execute("SELECT value FROM state WHERE key='workspace'").fetchone()
        if row is None:
            db.execute("INSERT INTO state(key,value) VALUES('workspace',?)", (json.dumps(seed_state()),))
        db.commit()

def read_state():
    init_db()
    with connect() as db:
        row = db.execute("SELECT value FROM state WHERE key='workspace'").fetchone()
        return json.loads(row["value"])

def write_state(state):
    with connect() as db:
        db.execute("INSERT INTO state(key,value) VALUES('workspace',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (json.dumps(state),))
        db.commit()

def reset_state():
    state = seed_state()
    write_state(state)
    return state
