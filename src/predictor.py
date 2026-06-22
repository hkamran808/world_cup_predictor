import joblib
import pandas as pd
class MatchPredictor:
    def __init__(self):
        self.model = joblib.load("models/best_xgb_model.pkl")
        self.scaler = joblib.load("models/scaler.pkl")
        self.matches = pd.read_csv("data\processed\matches_with_form.csv")

    def get_latest_team_stats(self, team):
        home_games = self.matches[self.matches["home_team"] == team]
        away_games = self.matches[self.matches["away_team"] == team]

        all_games = pd.concat([home_games, away_games])
        all_games = all_games.sort_values("date")
        latest_game = all_games.iloc[-1]
        if latest_game["home_team"] == team:
            return {
                "rank": latest_game["home_rank"],
                "points": latest_game["home_points"],
                "winrate": latest_game["home_last5_winrate"],
                "goals_scored": latest_game["home_last5_goals_scored"],
                "goals_conceded": latest_game["home_last5_goals_conceded"]
            }

        else:
            return {
                "rank": latest_game["away_rank"],
                "points": latest_game["away_points"],
                "winrate": latest_game["away_last5_winrate"],
                "goals_scored": latest_game["away_last5_goals_scored"],
                "goals_conceded": latest_game["away_last5_goals_conceded"]
            }
    
    def build_feature_vector(self, home_team, away_team):
        home = self.get_latest_team_stats(home_team)
        away = self.get_latest_team_stats(away_team)

        features = {
            "home_rank": home["rank"],
            "away_rank": away["rank"],
            "rank_diff": home["rank"] - away["rank"],
            "home_points": home["points"],
            "away_points": away["points"],
            "point_diff": home["points"] - away["points"],

            "home_last5_winrate": home["winrate"],
            "away_last5_winrate": away["winrate"],
            "home_last5_goals_scored": home["goals_scored"],
            "away_last5_goals_scored": away["goals_scored"],
            "home_last5_goals_conceded": home["goals_conceded"],
            "away_last5_goals_conceded": away["goals_conceded"],
            "home_last5_goal_diff": home["goals_scored"] - home["goals_conceded"],
            "away_last5_goal_diff": away["goals_scored"] - away["goals_conceded"],

            "tournament_weight": 4,

            "neutral": 1
        }

    def predict_match(self, home_team, away_team):
        features = self.build_feature_vector(home_team, away_team)
        X = pd.DataFrame([features])
        X_scaled = self.scaler.transform(X)

        proba = self.model.predict_proba(X_scaled)[0]

        return {
            "home_win": round(proba[2], 3),
            "away_win": round(proba[0], 3),
            "draw": round(proba[1], 3)
        }
    
if __name__ == "__main__":
    predictor = MatchPredictor()

    print(predictor.predict_match("France", "Brazil"))