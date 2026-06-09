import pandas as pd

results = pd.read_csv("data/raw/results.csv")
rankings = pd.read_csv("data/raw/fifa_rankings.csv")
world_cup = pd.read_csv("data/raw/world_cup.csv")

"""
print(results.shape)
print(rankings.shape)
print(world_cup.shape)

print(results.columns.tolist())
print(rankings.columns.tolist())
print(world_cup.columns.tolist())
"""
results["date"] = pd.to_datetime(results["date"])
rankings["rank_date"] = pd.to_datetime(rankings["rank_date"])
"""
print("Results Range:")
print(results["date"].min())
print(results["date"].max())

print("=" * 20)

print("Rankings Range:")
print(rankings["rank_date"].min())
print(rankings["rank_date"].max())

print("=" * 20)

print("unique teams (home, away) in results:")
print(results["home_team"].nunique())
print(results["away_team"].nunique())

print("unique countries in rankings:")
print(rankings["country_full"].nunique())
"""

from target_creation import create_target

results = create_target(results)

print(results[[
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "target"
]].head())