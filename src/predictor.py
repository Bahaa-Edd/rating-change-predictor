from math import ceil
from datetime import datetime


HALF_BAND = 0.05

def get_boundaries(avg):
    """Return (displayed, fall_boundary, rise_boundary) for a given average."""
    displayed=round(avg,1)
    return displayed, round(displayed-0.05, 2), round(displayed+0.05, 2)


def votes_to_boundary(avg, votes, new_rating, target):
    """Return how many new votes (rating new_rating each) push the average
        to target, or None if that can never happen."""
    if new_rating - target == 0:
        return None

    else:
        k=votes * (target - avg) / (new_rating - target)
        if k<=0:return None
        else: return ceil(k)


def implied_rating(avg1, votes1, avg2, votes2):
    """Return the average rating of the votes added between two snapshots,
    or None if no new votes arrived."""
    pts_before= votes1*avg1
    pts_after= votes2*avg2
    new_pts = pts_after-pts_before
    new_votes=votes2-votes1
    if(new_votes<=0):return None
    return new_pts/new_votes

def progress_pct(avg):
    """Return signed progress (-100 to +100) toward a rating change:
    positive toward a rise, negative toward a fall."""
    displayed=round(avg,1)
    return ((avg-displayed)/HALF_BAND)*100


def votes_per_hour(votes1, time1, votes2, time2):
    """Return how many votes per hour arrived between two snapshots,
    or None if the time between them is zero or negative."""
    timedelta= datetime.fromisoformat(time2)-datetime.fromisoformat(time1)
    deltahours = timedelta.total_seconds()/3600
    if(deltahours<=0):
        return None
    return (votes2-votes1)/deltahours


def hours_to_change(history):
    """history: list of (snapshot_time, vote_average, vote_count), oldest first.
    Return (direction, hours) where direction is "rise" or "fall",
    or None if no prediction is possible."""
    if len(history) < 2:
        return None

    time1, avg1, votes1 = history[0]
    time2, avg2, votes2 = history[-1]

    # 1. Who is voting? (rating of the new votes)
    rating = implied_rating(avg1, votes1, avg2, votes2)
    if rating is None:
        return None

    # 2. How fast? (votes per hour)
    speed = votes_per_hour(votes1, time1, votes2, time2)
    if not speed:
        return None

    # 3. Which boundary are they pushing toward?
    _, fall, rise = get_boundaries(avg2)
    if rating > avg2:
        direction, target = "rise", rise
    elif rating < avg2:
        direction, target = "fall", fall
    else:
        return None

    # 4. How many votes to get there, and how long that takes
    needed = votes_to_boundary(avg2, votes2, rating, target)
    if needed is None:
        return None

    return direction, needed / speed

