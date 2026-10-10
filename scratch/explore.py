import os, httpx
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}"}
base = "https://api.themoviedb.org/3"

r = httpx.get(f"{base}/movie/popular", headers=headers, params={"page": 1})
data = r.json()
print(r.status_code, data["page"], data["total_pages"], len(data["results"]))

movie_id = data["results"][0]["id"]
d = httpx.get(f"{base}/movie/{movie_id}", headers=headers).json()
print(d["title"], d["vote_average"], d["vote_count"])
print(r.headers)