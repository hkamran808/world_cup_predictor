import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st
from src.predictor import MatchPredictor

predictor = MatchPredictor()

home = st.text_input("Home Team")
away = st.text_input("Away Team")

if st.button("Predict"):
    result = predictor.predict_match(home, away)
    st.write(result)
    