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