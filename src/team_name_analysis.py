import pandas as pd

results = pd.read_csv("data/raw/results.csv")
rankings = pd.read_csv("data/raw/fifa_rankings.csv")

result_teams = set(results["home_team"].unique()) | set(results["away_team"].unique())
ranking_teams = set(rankings["country_full"].unique())

missing = sorted(result_teams - ranking_teams)

print(f"Result teams: {len(result_teams)}")
print(f"Ranking teams: {len(ranking_teams)}")
print(f"Missing teams: {len(missing)}")

for team in missing[:100]:
    print(team)