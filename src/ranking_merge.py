from turtle import home

import pandas as pd
from sqlalchemy import column
from streamlit import columns
from data_loader import load_data

results, rankings, world_cup, matches = load_data()

matches = matches.sort_values("date")
rankings = rankings.sort_values("rank_date")

home_matches = matches.copy()
home_matches = home_matches.rename(columns={"home_team": "country_full"})

home_matches = pd.merge_asof(
    home_matches,
    rankings,
    left_on="date",
    right_on="rank_date",
    by="country_full",
    direction="backward"
)
home_matches = home_matches.rename(columns={"rank": "home_rank", "total_points": "home_points"})

away_matches = matches.copy()
away_matches = away_matches.rename(columns={"away_team": "country_full"})

away_matches = pd.merge_asof(
    away_matches.sort_values("date"),
    rankings.sort_values("rank_date"),
    left_on="date",
    right_on="rank_date",
    by="country_full",
    direction="backward"
)
away_matches = away_matches.rename(columns={"rank": "away_rank", "total_points": "away_points"})

matches["home_rank"] = home_matches["home_rank"]
matches["home_points"] = home_matches["home_points"]
matches["away_rank"] = away_matches["away_rank"]
matches["away_points"] = away_matches["away_points"]

matches["rank_diff"] = (matches["home_rank"] - matches["away_rank"])
matches["point_diff"] = (matches["home_points"] - matches["away_points"])

#print(matches[["home_rank", "away_rank", "home_points", "away_points"]].isnull().sum())
#print(home_matches.shape)
#print(home_matches[["country_full","away_team","rank","total_points"]].head())
matches = matches.dropna(  # having 0.64 & 1.05% null values, so we drop them
    subset=[
        "home_rank",
        "away_rank",
        "home_points",
        "away_points"
])
#print(len(matches))

matches.to_csv("data/processed/matches_with_rankings.csv", index=False)