from data_loader import load_data

results, rankings, world_cup, matches = load_data()
matches = matches.sort_values("date")

from collections import defaultdict

team_history = defaultdict(list)

home_last5_winrate = []
away_last5_winrate = []

home_last5_goals_scored = []
away_last5_goals_scored = []

home_last5_goals_conceded = []
away_last5_goals_conceded = []

def compute_form(history):
    if len(history) == 0:
        return 0.5, 0, 0
    
    last5 = history[-5:]
    wins = sum(game["win"] for game in last5)
    winrate = wins / len(last5)

    goals_scored = sum(game["goals_scored"] for game in last5) / len(last5)
    goals_conceded = sum(game["goals_conceded"] for game in last5) / len(last5)

    return winrate, goals_scored, goals_conceded

for _, row in matches.iterrows():
    home = row["home_team"]
    away = row["away_team"]

    home_winrate, home_scored, home_conceded = compute_form(team_history[home])
    away_winrate, away_scored, away_conceded = compute_form(team_history[away])

    home_last5_winrate.append(home_winrate)
    away_last5_winrate.append(away_winrate)

    home_last5_goals_scored.append(home_scored)
    away_last5_goals_scored.append(away_scored)

    home_last5_goals_conceded.append(home_conceded)
    away_last5_goals_conceded.append(away_conceded)

    home_win = int(row["home_score"] > row["away_score"])
    team_history[home].append({
        "win": home_win,
        "goals_scored": row["home_score"],
        "goals_conceded": row["away_score"]
    })

    away_win = int(row["home_score"] < row["away_score"])
    team_history[away].append({
        "win": away_win,
        "goals_scored": row["away_score"],
        "goals_conceded": row["home_score"]
    })


matches["home_last5_winrate"] = home_last5_winrate
matches["away_last5_winrate"] = away_last5_winrate

matches["home_last5_goals_scored"] = home_last5_goals_scored
matches["away_last5_goals_scored"] = away_last5_goals_scored

matches["home_last5_goals_conceded"] = home_last5_goals_conceded
matches["away_last5_goals_conceded"] = away_last5_goals_conceded


#print(matches[["home_team", "away_team", "home_last5_winrate", "away_last5_winrate"]].head(10))
matches.to_csv("data/processed/matches_with_form.csv", index=False)