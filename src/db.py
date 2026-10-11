import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "market_watch.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS films (
                film_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                film_id INTEGER NOT NULL,
                snapshot_time TEXT NOT NULL,
                vote_average REAL NOT NULL,
                vote_count INTEGER NOT NULL,
                FOREIGN KEY (film_id) REFERENCES films(film_id)
            )
        """)


if __name__ == "__main__":
    create_tables()
    print("Database ready")