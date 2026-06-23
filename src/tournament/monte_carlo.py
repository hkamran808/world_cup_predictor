import random

def simulate_match(probabilities):
    outcome = random.choices(
        population=["home_win", "draw", "away_win"],
        weights=[probabilities["home_win"], probabilities["draw"], probabilities["away_win"]],
        k=1
    )[0]
    return outcome

from predictor import MatchPredictor

predictor = MatchPredictor()
for _ in range(10):
    probabilities = predictor.predict_match("France", "Brazil")
    print(probabilities)