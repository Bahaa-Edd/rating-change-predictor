import os
import time

import httpx
from dotenv import load_dotenv

import sqlite3
from pathlib import Path

from db import get_connection

load_dotenv()

base_url = "https://api.themoviedb.org/3"
headers = {"Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}"}

DB_PATH = Path("data/market_watch.db")


def fetch_page(endpoint, page):
    response = httpx.get(f"{base_url}{endpoint}", headers=headers, params={"page": page}, )
    response.raise_for_status()
    time.sleep(0.3)  # be polite: stay under TMDB's rate limit
    return response.json()["results"]



if __name__ == "__main__":
    films = {}
    endpoints=["/movie/popular","/movie/now_playing","/trending/movie/day"]
    for i in endpoints:
        for j in range(1,6):
            movies= fetch_page(i, j)
            for movie in movies:
                films[movie["id"]] = movie["title"]
    print(len(films))
    with get_connection() as conn:
        for film_id, title in films.items():
            conn.execute(
                "INSERT OR IGNORE INTO films (film_id, title) VALUES (?, ?)",
                (film_id, title),
            )