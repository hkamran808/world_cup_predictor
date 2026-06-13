import pandas as pd

rankings = pd.read_csv("data/raw/fifa_rankings.csv")

teams = set(rankings["country_full"].unique())
#for team in teams:
#   print(team)
"""
print("United States", "United States" in teams)
print("USA", "USA" in teams) #true

print("Congo DR", "Congo DR" in teams) #true
print("DR Congo", "DR Congo" in teams) 

print("Korea Republic", "Korea Republic" in teams) # true
print("South Korea", "South Korea" in teams) 

print("IR Iran", "IR Iran" in teams) # true
print("Iran", "Iran" in teams) 

print("Kyrgyz Republic", "Kyrgyz Republic" in teams) # true
print("Kyrgyzstan", "Kyrgyzstan" in teams) 

print("Cape Verde Islands", "Cape Verde Islands" in teams)
print("Cape Verde", "Cape Verde" in teams)
"""
"""
for team in teams:  #none
    if "Cape" in team:
        print(team)

count = 0
for team in teams: # got it
    if "Verde" in team:
        print(team)
        count += 1
print(count)
"""
# quick re-check
matches = pd.read_csv("data/processed/fifa_matches_only.csv")
print(matches.shape)