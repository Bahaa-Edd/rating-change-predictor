from db import get_connection

def get_film_history(film_id):
    """Return a list of (snapshot_time, vote_average, vote_count)
    for one film, oldest first, ignoring zero-vote snapshots."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT snapshot_time, vote_average, vote_count
               FROM snapshots
               WHERE film_id = ? AND vote_count > 0
               ORDER BY snapshot_time ASC""",
            (film_id,),
        ).fetchall()
    return rows




if __name__ == "__main__":
    history = get_film_history(105)  # Back to the Future
    print(len(history), "snapshots")
    print(history[0])
    print(history[-1])