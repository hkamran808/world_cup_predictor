import pandas as pd


def create_target(df):
    df = df.copy()

    df["target"] = 1

    df.loc[df["home_score"] > df["away_score"], "target"] = 2
    df.loc[df["home_score"] < df["away_score"], "target"] = 0

    return df