import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.predictor import MatchPredictor

st.set_page_config(
    page_title="International Football Match Predictor & World Cup Simulator",
    page_icon="⚽",
    layout='wide'
)

@st.cache_resource
def load_predictor():
    return MatchPredictor()

predictor = load_predictor()

st.sidebar.title("⚽ International Football Match Predictor & World Cup Simulator")
page = st.sidebar.radio(
    "Navigation",
    [
        "Match Predictor",
        "Tournament Simulator",
        "About"
    ]
)
st.sidebar.markdown("---")
st.sidebar.metric("Model", "XGBoost")
st.sidebar.metric("Accuracy", "54%")
st.sidebar.metric("Training Matches", "26,866")

if page == "Match Predictor":
    st.title("⚽ Match Predictor")
    st.write("*Predict international football matches using machine learning*")

    teams = sorted(predictor.matches["home_team"].unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        home = st.selectbox("Home Team", teams, index=teams.index("France"))
    with col2:
        away = st.selectbox("Away Team", teams, index=teams.index("Brazil"))

    neutral = st.checkbox("Neutral Venue", value=True)

    tournament = st.selectbox(
        "Tournament",
        [
            "FIFA World Cup",
            "Friendly",
            "Continental Cup",
            "Qualification"
        ]
    )
    if st.button("Predict Match"):
        with st.spinner("Running prediction..."):
            result = predictor.predict_match(home, away)

    winner = max(result, key=result.get)

    if winner == "draw":
        st.info("The model expects a closely contested match")

    winner_name = {
        'home_win': home,
        'away_win': away,
        'draw': 'Draw'
    }
    st.success(f"🏆 Predicted Winner: {winner_name[winner]}")

    c1, c2, c3 = st.columns(3)
    c1.metric(home, f"{result['home_win']*100:.1f}%")
    c2.metric("Draw", f"{result['draw']*100:.1f}%")
    c3.metric(away,f"{result['away_win']*100:.1f}%")

    df = pd.DataFrame({
        "Outcome":[
            home,
            "Draw",
            away
        ],

        "Probability":[
            result["home_win"]*100,
            result["draw"]*100,
            result["away_win"]*100
        ]
    })

    fig = px.bar(
        df,
        x="Outcome",
        y="Probability",
        text="Probability"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Model Interpretation")
    home_stats = predictor.get_latest_team_stats(home)
    away_stats = predictor.get_latest_team_stats(away)

    reasons = []
    if home_stats["rank"] < away_stats["rank"]:
        reasons.append(f"{home} has the better FIFA ranking")
    elif home_stats["rank"] > away_stats["rank"]:
        reasons.append(f"{away} has the better FIFA ranking")

    if home_stats["winrate"] > away_stats["winrate"]:
        reasons.append(f"{home} has stronger recent form")
    elif home_stats["winrate"] < away_stats["winrate"]:
        reasons.append(f"{away} has stronger recent form")

    if (home_stats["goals_scored"] > away_stats["goals_scored"]):
        reasons.append(f"{home} scores more goals recently")
    elif (home_stats["goals_scored"] < away_stats["goals_scored"]):
        reasons.append(f"{away} scores more goals recently")

    if home_stats["goals_conceded"] < away_stats["goals_conceded"]:
        reasons.append(f"{home} has the stronger recent defense")
    elif away_stats["goals_conceded"] < home_stats["goals_conceded"]:
        reasons.append(f"{away} has the stronger recent defense")


    if len(reasons) == 0:
        st.write("The two teams appear evenly matched according to the available features")
    for reason in reasons:
        st.write("✅", reason)

elif page == "Tournament Simulator":
    st.title("🏆 Tournament Simulator")
    mode = st.radio(
        "Mode",
        [
            "Official 2026",
            "Custom"
        ]
    )

from src.tournament.teams import OFFICIAL_TEAMS
from src.tournament.group_stage import generate_groups

if mode == "Official 2026":
    selected_teams = OFFICIAL_TEAMS
else:
    selected_teams = st.multiselect("Choose 48 Teams", teams, default=teams[:48])

if st.button("Randomize Groups"):
    st.write("Randomizing groups...")
    groups = generate_groups(selected_teams)

for group_name, group_teams in groups.items():
    st.subheader(f"Group {group_name}")
    for team in group_teams:
        #st.write(team)
        st.selectbox("", teams, index=teams.index(team, key=f"{group_name}_{team}"))

if st.button("Simulate Tournament"):
    st.write("Simulating tournament...")
    

"""
home = st.text_input("Home Team")
away = st.text_input("Away Team")

if st.button("Predict"):
    result = predictor.predict_match(home, away)
    st.write(result)
"""