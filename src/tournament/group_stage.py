import random

def generate_groups(teams):
    teams = teams.copy()
    random.shuffle(teams)

    groups = {}
    letters = "ABCDEFGHIJKL"
    for i in range(12):
        groups[letters[i]] = teams[i*4:(i+1)*4]
    return groups