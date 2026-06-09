import pandas as pd

def load_data():
    results = pd.read_csv("data/raw/results.csv")
    rankings = pd.read_csv("data/raw/fifa_rankings.csv")
    world_cup = pd.read_csv("data/raw/world_cup.csv")

    results["date"] = pd.to_datetime(results["date"])
    rankings["rank_date"] = pd.to_datetime(rankings["rank_date"])

    return results, rankings, world_cup