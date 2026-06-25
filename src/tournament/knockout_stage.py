from matplotlib.pylab import ranf

from src.predictor import MatchPredictor
from src.tournament.monte_carlo import simulate_match

predictor = MatchPredictor()

def simulate_knockout_match(team1, team2):
    probabilities = predictor.predict_match(team1, team2)
    result = simulate_match(probabilities)

    if result == "home_win":
        return team1
    elif result == "away_win":
        return team2
    else:
        # to be more realistic, we'll just simulate it as if it is penalty shootout with random module
        import random
        return random.choice([team1, team2])
    
for _ in range(10):
    print(simulate_knockout_match("France", "Brazil"))


#mini world cup bracket style from semi finalss
semi_finalists = [
    "France",
    "Brazil",
    "Argentina",
    "England"
]

finalist1 = simulate_knockout_match(semi_finalists[0], semi_finalists[1])
finalist2 = simulate_knockout_match(semi_finalists[2], semi_finalists[3])

champ = simulate_knockout_match(finalist1, finalist2)

print(champ)