from data_loader import load_data

results, rankings, world_cup = load_data()
results = results[results["date"] >= "1993-01-01"]

from team_mapping import TEAM_MAPPING
results["home_team"] = results["home_team"].replace(TEAM_MAPPING)
results["away_team"] = results["away_team"].replace(TEAM_MAPPING)

result_teams = (set(results["home_team"].unique()) | set(results["away_team"].unique()))
ranking_teams = set(rankings["country_full"].unique())

missing = sorted(result_teams - ranking_teams)

print(f"Missing teams: {len(missing)}")
print(missing)