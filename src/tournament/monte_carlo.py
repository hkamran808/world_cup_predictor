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

probabilities = predictor.predict_match("France", "Brazil")

results = {
    "home_win": 0,
    "draw": 0,
    "away_win": 0
}

for _ in range(10000):
    result = simulate_match(probabilities)
    results[result] += 1

print(results)