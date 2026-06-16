import pandas as pd

def load_data():
    results = pd.read_csv("data/raw/results.csv")
    rankings = pd.read_csv("data/raw/fifa_rankings.csv")
    world_cup = pd.read_csv("data/raw/world_cup.csv")
    matches = pd.read_csv("data/processed/matches_with_rankings.csv")

    matches1 = pd.read_csv("data/processed/matches_with_form.csv")

    results["date"] = pd.to_datetime(results["date"])
    rankings["rank_date"] = pd.to_datetime(rankings["rank_date"])
    matches["date"] = pd.to_datetime(matches["date"])
    matches1["date"] = pd.to_datetime(matches1["date"])

    return results, rankings, world_cup, matches, matches1