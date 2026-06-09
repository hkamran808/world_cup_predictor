import pandas as pd

results = pd.read_csv("data/raw/results.csv")

results["date"] = pd.to_datetime(results["date"])
results = results[results["date"] >= "1993-01-01"]

print(f"Filtered results shape: {results.shape}")

print(f"Top 30 tournaments:")
print(results["tournament"].value_counts().head(30))

# Filter to only include important matches
IMPORTANT_TOURNAMENTS = [
    "FIFA World Cup",
    "FIFA World Cup qualification",
    "UEFA Euro",
    "UEFA Euro qualification",
    "Copa América",
    "AFC Asian Cup",
    "AFC Asian Cup qualification",
    "African Cup of Nations",
    "African Cup of Nations qualification",
    "Gold Cup",
    "UEFA Nations League",
    "CONCACAF Nations League",
    "Confederations Cup",
    "Oceania Nations Cup"
]

results = results[results["tournament"].isin(IMPORTANT_TOURNAMENTS)]