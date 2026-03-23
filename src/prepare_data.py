import json
from pathlib import Path
import pandas as pd


def load_matches(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["matches"]


def extract_match_info(matches: list) -> pd.DataFrame:
    rows = []  # create empty list

    for match in matches:  # loop over matches
        row = {
            "match_id": match["id"],
            "utc_date": match["utcDate"],
            "status": match["status"],
            "matchday": match["matchday"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "home_score": match["score"]["fullTime"]["home"],
            "away_score": match["score"]["fullTime"]["away"],
            "winner": match["score"]["winner"]
        }
        rows.append(row)

    return pd.DataFrame(rows)


def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    input_file = "data/raw/pl_matches_2025.json"
    output_file = "data/processed/pl_matches_2025.csv"

    matches = load_matches(input_file)
    df = extract_match_info(matches)
    save_dataframe(df, output_file)

    print(df.head())
    print(f"Saved {output_file}")