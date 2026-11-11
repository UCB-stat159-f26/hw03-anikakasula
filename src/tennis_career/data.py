import requests
import json
import re
import pandas as pd

def _normalize_name(player_name):
    """Convert player names to Tennis Abstract's URL format."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Please provide a valid player name.")

    parts = player_name.strip().split()

    if len(parts) > 1:
        return "".join(word.capitalize() for word in parts)

    return parts[0][0].upper() + parts[0][1:]


def _download_career_js(player_name):
    """Download a player's career match JavaScript file."""
    player_id = _normalize_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 404:
            raise ValueError(
                f"No career data found for '{player_name}'. Check the spelling."
            )

        response.raise_for_status()

    except requests.RequestException as error:
        raise ConnectionError(f"Unable to download data: {error}") from error

    return response.text


def _parse_career_js(js_content):
    """Extract match records from Tennis Abstract JavaScript."""
    match = re.search(r"var\s+morematchmx\s*=\s*", js_content)

    if not match:
        raise ValueError("No career match data found in JS file.")

    try:
        data = js_content[match.end():].lstrip()
        records, _ = json.JSONDecoder().raw_decode(data)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("Unable to parse career match data.") from error

    if not isinstance(records, list):
        raise ValueError("Career match data must be a list.")

    return records

def _opponent_age(raw_value, match_date):
    """Calculate opponent age from birth date or existing age."""
    value = str(raw_value).strip()

    if re.fullmatch(r"\d{8}", value):
        birth_date = pd.to_datetime(
            value, format="%Y%m%d", errors="coerce"
        )
        if pd.isna(birth_date) or pd.isna(match_date):
            return float("nan")
        return (match_date - birth_date).days / 365.2425

    return pd.to_numeric(value, errors="coerce")
