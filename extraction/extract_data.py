
import json
import csv
from pathlib import Path

# Project paths
INPUT_FOLDER = Path("data/raw/ipl_json")
OUTPUT_FOLDER = Path("data/processed")
OUTPUT_FILE = OUTPUT_FOLDER / "deliveries.csv"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

columns = [
    "match_id", "date", "season", "venue",
    "batting_team", "bowling_team", "innings",
    "over", "ball", "batter", "bowler",
    "non_striker", "batter_runs", "extras",
    "total_runs", "is_wicket", "dismissal_kind",
    "player_out"
]

json_files = list(INPUT_FOLDER.rglob("*.json"))

if not json_files:
    raise FileNotFoundError(
        f"No JSON files found in {INPUT_FOLDER.resolve()}"
    )

total_rows = 0
failed_files = []

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                match = json.load(f)

            info = match.get("info", {})
            teams = info.get("teams", [])
            dates = info.get("dates", [])
            match_date = str(dates[0]) if dates else ""
            season = match_date[:4] if match_date else ""
            venue = info.get("venue", "")

            for innings_number, innings_data in enumerate(
                match.get("innings", []), start=1
            ):
                batting_team = innings_data.get("team", "")
                bowling_team = next(
                    (team for team in teams if team != batting_team), ""
                )

                for over_data in innings_data.get("overs", []):
                    over_number = over_data.get("over", 0)

                    for ball_number, delivery in enumerate(
                        over_data.get("deliveries", []), start=1
                    ):
                        runs = delivery.get("runs", {})
                        wickets = delivery.get("wickets", [])
                        first_wicket = wickets[0] if wickets else {}

                        writer.writerow({
                            "match_id": file.stem,
                            "date": match_date,
                            "season": season,
                            "venue": venue,
                            "batting_team": batting_team,
                            "bowling_team": bowling_team,
                            "innings": innings_number,
                            "over": over_number,
                            "ball": ball_number,
                            "batter": delivery.get("batter", ""),
                            "bowler": delivery.get("bowler", ""),
                            "non_striker": delivery.get("non_striker", ""),
                            "batter_runs": runs.get("batter", 0),
                            "extras": runs.get("extras", 0),
                            "total_runs": runs.get("total", 0),
                            "is_wicket": 1 if wickets else 0,
                            "dismissal_kind": first_wicket.get(
                                "kind", ""
                            ),
                            "player_out": first_wicket.get(
                                "player_out", ""
                            )
                        })

                        total_rows += 1

        except Exception as error:
            failed_files.append((file.name, str(error)))

print("\n====================================")
print("CRICKET DATA EXTRACTION COMPLETED")
print("====================================")
print("JSON files found:", len(json_files))
print("Delivery records extracted:", total_rows)
print("Files with errors:", len(failed_files))
print("Output file:", OUTPUT_FILE.resolve())

for filename, error in failed_files[:10]:
    print("ERROR:", filename, "-", error)
