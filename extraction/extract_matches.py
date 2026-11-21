
import json
import csv
from pathlib import Path

INPUT_FOLDER = Path("data/raw/ipl_json")
OUTPUT_FOLDER = Path("data/processed")
OUTPUT_FILE = OUTPUT_FOLDER / "matches.csv"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

columns = [
    "match_id",
    "date",
    "season",
    "venue",
    "team1",
    "team2",
    "toss_winner",
    "toss_decision",
    "winner",
    "result_type",
    "result_margin",
    "player_of_match",
    "event_name"
]

json_files = list(INPUT_FOLDER.rglob("*.json"))
total_matches = 0
failed_files = []

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()

    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as json_file:
                match = json.load(json_file)

            info = match.get("info", {})
            dates = info.get("dates", [])
            teams = info.get("teams", [])
            toss = info.get("toss", {})
            outcome = info.get("outcome", {})

            winner = outcome.get("winner", "")
            margin = outcome.get("by", {})

            result_type = (
                "Win" if winner
                else outcome.get("result", "No Result")
            )

            margin_text = ""
            if "runs" in margin:
                margin_text = f"{margin['runs']} runs"
            elif "wickets" in margin:
                margin_text = f"{margin['wickets']} wickets"

            player_of_match = info.get("player_of_match", [])
            if isinstance(player_of_match, list):
                player_of_match = ", ".join(player_of_match)

            match_date = str(dates[0]) if dates else ""

            writer.writerow({
                "match_id": file.stem,
                "date": match_date,
                "season": match_date[:4],
                "venue": info.get("venue", ""),
                "team1": teams[0] if len(teams) > 0 else "",
                "team2": teams[1] if len(teams) > 1 else "",
                "toss_winner": toss.get("winner", ""),
                "toss_decision": toss.get("decision", ""),
                "winner": winner,
                "result_type": result_type,
                "result_margin": margin_text,
                "player_of_match": player_of_match,
                "event_name": info.get("event", {}).get("name", "")
            })

            total_matches += 1

        except Exception as error:
            failed_files.append((file.name, str(error)))

print("MATCH EXTRACTION COMPLETED!")
print("JSON files found:", len(json_files))
print("Matches extracted:", total_matches)
print("Files with errors:", len(failed_files))
print("Output:", OUTPUT_FILE.resolve())

for filename, error in failed_files[:10]:
    print("ERROR:", filename, error)
