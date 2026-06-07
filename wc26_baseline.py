import pandas as pd

ranking_files = [
    "fifa_ranking_2022-10-06.csv",
    "fifa_ranking_2023-07-20.csv",
    "fifa_ranking_2024-04-04.csv",
    "fifa_ranking_2024-06-20.csv"
]

rankings = pd.concat([pd.read_csv(file) for file in ranking_files], ignore_index=True)
rankings["rank_date"] = pd.to_datetime(rankings["rank_date"])

rankings.to_csv("fifa_rankings_combined.csv", index=False)

#quick check
print(rankings.shape)
print(rankings["rank_date"].unique())
print(rankings.head())