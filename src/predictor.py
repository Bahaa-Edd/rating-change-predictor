from math import ceil

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


