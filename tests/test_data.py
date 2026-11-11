from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import patch
from tennis_career.data import _download_career_js

from tennis_career.data import _parse_career_js, _opponent_age, _clean_matches


def test_female_data():
    path = Path(__file__).parent / "fixtures/FemalePlayerCareer.js"
    matches = _parse_career_js(path.read_text())

    assert len(matches) == 3
    assert matches[0][11] == "Anne Miller"

    data = _clean_matches(matches, pd.Timestamp("1981-09-26"))
    assert len(data) == 3
    assert data.iloc[0]["opponent_age"] == pytest.approx(18.78, abs=0.01)


def test_male_data():
    path = Path(__file__).parent / "fixtures/MalePlayerCareer.js"
    matches = _parse_career_js(path.read_text())

    assert len(matches) == 3
    assert matches[0][11] == "Guillermo Platel"

    data = _clean_matches(matches, pd.Timestamp("1986-06-03"))
    assert len(data) == 3
    assert data.iloc[0]["opponent_age"] == pytest.approx(22.26, abs=0.01)


def test_invalid_js():
    with pytest.raises(ValueError):
        _parse_career_js("invalid data")


def test_missing_opponent_age():
    date = pd.Timestamp("2001-09-10")
    age = _opponent_age("", date)

    assert pd.isna(age)

def test_invalid_player():
    with patch("tennis_career.data.requests.get") as get:
        get.return_value.status_code = 404

        with pytest.raises(ValueError, match="not found"):
            _download_career_js("Gaston Sanchez")
