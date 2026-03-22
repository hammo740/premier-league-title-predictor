import os 
import json
from pathlib import Path
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
COMPETITION = "PL"

def fetch_matches (season: int = 2025) -> dict:
    if not API_KEY:
        raise ValueError("FOOTBALL_DATA_API_KEY saknas i .env")
    
    url = f"{BASE_URL}/competitions/{COMPETITION}/matches"
    headers = {"X-Auth-Token": API_KEY}
    params = {"season": season}

    response = requests.get(url, headers = headers, params = params, timeout = 30)
    response.raise_for_status()
    return response.json()

def save_json(data: dict, filename: str) -> None:
    output_dir = Path("data/raw")
    output_dir.mkdir(parents = True, exist_ok = True )
    
    output_path = output_dir / filename
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        

if __name__ == "__main__":
    season = 2025
    data = fetch_matches(season=season)
    save_json(data, f"pl_matches_{season}.json")
    print(f"Saved data/raw/pl_matches_{season}.json")