from data_loader import load_data

results, rankings, world_cup = load_data()
results = results[results["date"] >= "1993-01-01"]

from team_mapping import TEAM_MAPPING
results["home_team"] = results["home_team"].replace(TEAM_MAPPING)
results["away_team"] = results["away_team"].replace(TEAM_MAPPING)

ranking_teams = set(rankings["country_full"].unique())

results = results[results["home_team"].isin(ranking_teams)]
results = results[results["away_team"].isin(ranking_teams)]

print(results.shape)

results.to_csv("data/processed/fifa_matches_only.csv", index=False)