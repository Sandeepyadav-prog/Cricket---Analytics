# Cricket Analytics – Data Dictionary

This document describes the six analytical datasets generated through the Gold layer of the project.

## 1. gold_batting_stats.csv
- season: IPL season
- batter: Player name
- total_runs: Total runs scored
- delivery_records: Number of delivery records
- fours: Number of fours
- sixes: Number of sixes
- dismissals: Recorded dismissals
- runs_per_100_delivery_records: Runs per 100 delivery records

## 2. gold_bowling_stats.csv
- season: IPL season
- bowler: Bowler name
- wickets: Recorded dismissals credited in the dataset aggregation
- runs_conceded: Aggregated runs
- delivery_records: Number of delivery records

## 3. gold_team_innings.csv
- match_id: Unique match identifier
- season: IPL season
- date: Match date
- venue: Match venue
- batting_team: Team batting in the innings
- innings: Innings number
- innings_total_runs: Total innings runs
- delivery_records: Number of delivery records
- wickets_lost: Recorded wickets lost

## 4. gold_venue_stats.csv
- venue: Stadium or venue name
- matches_played: Number of matches represented
- average_innings_score: Average innings score
- highest_innings_score: Highest innings score

## 5. gold_phase_analysis.csv
- season: IPL season
- batting_team: Batting team
- phase: Powerplay, Middle Overs, or Death Overs
- total_runs: Runs scored in the phase
- total_wickets: Recorded wickets
- delivery_records: Number of delivery records
- runs_per_delivery_record: Average runs per delivery record

## 6. gold_team_performance.csv
- team: Team name
- matches: Matches represented
- wins: Matches won
- losses: Matches lost
- ties: Tied matches
- no_results: Matches with no result
- win_percentage: Team win percentage

## Important Metric Note

The batting and bowling metrics are calculated from the available ball-by-ball records. They are analytical project metrics and may differ from official cricket statistics because of delivery and dismissal rules.
