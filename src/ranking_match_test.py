import pandas as pd
from team_mapping import TEAM_MAPPING
from data_loader import load_data

results, rankings, world_cup = load_data()

results["date"] = pd.to_datetime(results["date"])
rankings["rank_date"] = pd.to_datetime(rankings["rank_date"])

results = results[results["date"] >= "1993-01-01"]

results["home_team"] = results["home_team"].replace(TEAM_MAPPING)
results["away_team"] = results["away_team"].replace(TEAM_MAPPING)

ranking_teams = set(rankings["country_full"].unique())

home_missing = (~results["home_team"].isin(ranking_teams)).sum()

away_missing = (~results["away_team"].isin(ranking_teams)).sum()

print("Missing home:", home_missing)
print("Missing away:", away_missing)