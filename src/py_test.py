import pytest
from predictor import *

def test_boundaries():
    assert get_boundaries(8.381) == (8.4, 8.35, 8.45)

def test_rise():
    assert votes_to_boundary(8.381, 4771, 9.0, 8.45) == 599

def test_fall():
    assert votes_to_boundary(8.381, 4771, 5.0, 8.35) == 45

def test_impossible_rise():
    assert votes_to_boundary(8.381, 4771, 8.0, 8.45) is None


def test_implied_rating_clean():
    # 800 points -> 1700 points from 100 new votes = 9.0 each
    assert implied_rating(8.0, 100, 8.5, 200) == 9.0

def test_implied_rating_brand_new_day():
    assert implied_rating(8.364, 4651, 8.374, 4717) == pytest.approx(9.08, abs=0.01)

def test_no_new_votes():
    assert implied_rating(8.374, 4717, 8.374, 4717) is None



def test_progress_center():
    assert progress_pct(8.4) == 0

def test_progress_toward_fall():
    assert progress_pct(8.381) == pytest.approx(-38, abs=0.5)

def test_progress_toward_rise():
    assert progress_pct(8.425) == pytest.approx(50, abs=0.5)


def test_votes_per_hour():
    assert votes_per_hour(
        100, "2026-10-10T00:00:00+00:00",
        220, "2026-10-10T12:00:00+00:00",
    ) == 10.0

def test_votes_per_hour_same_time():
    assert votes_per_hour(
        100, "2026-10-10T00:00:00+00:00",
        150, "2026-10-10T00:00:00+00:00",
    ) is None




def test_hours_to_change_rise():
    history = [
        ("2026-10-10T00:00:00+00:00", 8.0, 100),
        ("2026-10-10T10:00:00+00:00", 8.5, 200),
    ]
    direction, hours = hours_to_change(history)
    assert direction == "rise"
    assert hours == pytest.approx(2.3, abs=0.01)

def test_hours_to_change_fall():
    history = [
        ("2026-10-10T00:00:00+00:00", 9.0, 100),
        ("2026-10-10T10:00:00+00:00", 8.5, 200),
    ]
    direction, hours = hours_to_change(history)
    assert direction == "fall"
    assert hours == pytest.approx(2.3, abs=0.01)

def test_hours_to_change_no_new_votes():
    history = [
        ("2026-10-10T00:00:00+00:00", 8.5, 200),
        ("2026-10-10T10:00:00+00:00", 8.5, 200),
    ]
    assert hours_to_change(history) is None


def test_last_window_drops_old_rows():
    history = [
        ("2026-10-10T00:00:00+00:00", 8.0, 100),
        ("2026-10-10T10:00:00+00:00", 8.2, 150),
        ("2026-10-11T06:00:00+00:00", 8.4, 220),
    ]
    window = last_window(history, 24)
    # newest row is 30h after the first, so the first row drops out
    assert len(window) == 2
    assert window[0][2] == 150   # oldest kept row
    assert window[-1][2] == 220  # newest row


def test_last_window_keeps_row_exactly_at_limit():
    history = [
        ("2026-10-10T00:00:00+00:00", 8.0, 100),
        ("2026-10-11T00:00:00+00:00", 8.4, 220),
    ]
    # exactly 24h apart: not older than the limit, so it stays
    assert len(last_window(history, 24)) == 2


def test_last_window_empty():
    assert last_window([], 24) == []