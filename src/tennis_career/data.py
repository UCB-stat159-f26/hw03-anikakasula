import requests
import json
import re
import pandas as pd

def _normalize_name(player_name):
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Please provide a valid player name.")

    parts = player_name.strip().split()

    if len(parts) > 1:
        return "".join(word.capitalize() for word in parts)

    return parts[0][0].upper() + parts[0][1:]



def _download_career_js(player_name):
    player_id = _normalize_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 404:
            raise ValueError(f"Player '{player_name}' not found.")
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Could not get player data: {e}") from e

    return response.text


def _parse_career_js(js_content):
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
    value = str(raw_value).strip()

    if re.fullmatch(r"\d{8}", value):
        birth_date = pd.to_datetime(
            value, format="%Y%m%d", errors="coerce"
        )
        if pd.isna(birth_date) or pd.isna(match_date):
            return float("nan")
        return (match_date - birth_date).days / 365.2425

    return pd.to_numeric(value, errors="coerce")

def _get_player_birth_date(player_name):
    name = _normalize_name(player_name).lower()

    for tour in ["wta", "atp"]:
        url = (f"https://raw.githubusercontent.com/micahp/"
               f"tennis-point-by-point-archive/main/{tour}/{tour}_players.csv")

        players = pd.read_csv(url, usecols=["name_first", "name_last", "dob"], dtype={"dob": "string"})
        names = players["name_first"].fillna("") + players["name_last"].fillna("")
        names = names.str.lower().str.replace(" ", "", regex=False)
        match = players[names == name]

        if not match.empty:
            dob = pd.to_datetime(match.iloc[0]["dob"],
                                 format="%Y%m%d", errors="coerce")
            if pd.notna(dob):
                return dob

    raise ValueError(f"Birth date not found for {player_name}")


def _clean_matches(matches, birth_date):
    rows = []

    for match in matches:
        if len(match) < 17 or match[4] not in ["W", "L"]:
            continue

        date = pd.to_datetime(match[0], format="%Y%m%d", errors="coerce")
        if pd.isna(date):
            continue

        opponent_age = _opponent_age(match[16], date)
        if pd.isna(opponent_age):
            continue

        player_age = (date - birth_date).days / 365.2425

        rows.append({
            "match_date": date,
            "player_age": player_age,
            "opponent_age": opponent_age,
            "age_difference": player_age - opponent_age,
            "result": match[4]
        })

    return pd.DataFrame(rows)


def get_career_matches(player_name):
    js_content = _download_career_js(player_name)
    matches = _parse_career_js(js_content)
    birth_date = _get_player_birth_date(player_name)

    data = _clean_matches(matches, birth_date)

    if data.empty:
        raise ValueError(f"No usable matches found for {player_name}")

    return data
