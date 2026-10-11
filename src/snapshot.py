import os
import time
from typing import Any

import httpx
from dotenv import load_dotenv

import sqlite3
from pathlib import Path

from datetime import datetime, timezone
from db import get_connection

load_dotenv()

base_url = "https://api.themoviedb.org/3"
headers = {"Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}"}


def get_films():
    with get_connection() as conn:
        rows = conn.execute("SELECT film_id, title FROM films").fetchall()
    return rows


def get_movie_stats(film_id):
    r = httpx.get(f"{base_url}/movie/{film_id}", headers=headers)
    r.raise_for_status()
    time.sleep(0.3)  # be polite: stay under TMDB's rate limit
    data = r.json()
    return {"rating_avg": data["vote_average"], "vote_count": data["vote_count"]}


def get_all_stats(films: object) -> dict[Any, Any]:
    stats = {}
    for film_id, title in films:
        stats[film_id] = get_movie_stats(film_id)
    return stats

def save_stats(stats: dict[Any, Any]):
    snapshot_time= datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        for film_id, rating in stats.items():
            conn.execute(
                "INSERT INTO snapshots (film_id, snapshot_time, vote_average, vote_count) VALUES (?, ?, ?, ?)",
                (film_id, snapshot_time, rating["rating_avg"], rating["vote_count"]),
            )


if __name__ == "__main__":
    films = get_films()
    stats = get_all_stats(films)
    print(len(stats), "films fetched")
    print(stats[105])
    save_stats(stats)


