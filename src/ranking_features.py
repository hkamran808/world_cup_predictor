from data_loader import load_data

results, rankings, world_cup = load_data()
results = results[results["date"] >= "1993-01-01"]

from team_mapping import TEAM_MAPPING
results["home_team"] = results["home_team"].replace(TEAM_MAPPING)
results["away_team"] = results["away_team"].replace(TEAM_MAPPING)

def get_team_ranking_on_date(team, date, rankings):
    team_rankings = rankings[(rankings["country_full"] == team) & (rankings["rank_date"] <= date)]

    if team_rankings.empty:
        return None, None

    latest = team_rankings.sort_values("rank_date").iloc[-1]
    return latest["rank"], latest["total_points"]


home_ranks = []
away_ranks = []

home_points = []
away_points = []

missing_home = set()
missing_away = set()

for _, row in results.iterrows():
    h_rank, h_points = get_team_ranking_on_date(row["home_team"], row["date"], rankings)

    a_rank, a_points = get_team_ranking_on_date(row["away_team"], row["date"], rankings)

    if h_rank is None:
        missing_home.add(row["home_team"])
        
    if a_rank is None:
        missing_away.add(row["away_team"])

    home_ranks.append(h_rank)
    away_ranks.append(a_rank)
    home_points.append(h_points)
    away_points.append(a_points)

print(f"Missing home teams: {len(missing_home)}")
print(sorted(missing_home))
print("=" * 20)
print(f"Missing away teams: {len(missing_away)}")
print(sorted(missing_away))

results["home_rank"] = home_ranks
results["away_rank"] = away_ranks
results["home_points"] = home_points
results["away_points"] = away_points
results["rank_diff"] = results["home_rank"] - results["away_rank"]
results["points_diff"] = results["home_points"] - results["away_points"]

results.to_csv("data/processed/matches_with_rankings.csv", index=False)