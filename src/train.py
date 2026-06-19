from data_loader import load_data
results, rankings, world_cup, matches, matches1 = load_data()

#print(matches1.columns.tolist())
FEATURES = [
    "home_rank",
    "away_rank",
    "rank_diff",

    "home_points",
    "away_points",
    "point_diff",

    "home_last5_winrate",
    "away_last5_winrate",

    "home_last5_goals_scored",
    "away_last5_goals_scored",

    "home_last5_goals_conceded",
    "away_last5_goals_conceded",

    "neutral"
]

matches1["target"] = 1

matches1.loc[matches1["home_score"] > matches1["away_score"], "target"] = 2
matches1.loc[matches1["home_score"] < matches1["away_score"], "target"] = 0
TARGET = "target"

#since football is temporal data, we will split on size but not randomly
matches1 = matches1.sort_values("date")
matches1 = matches1.dropna(subset=FEATURES + [TARGET])  # we drop rows with missing values in features or target
split = int(len(matches1) * 0.8)

train = matches1.iloc[:split]
test = matches1.iloc[split:]

X_train, y_train, X_test, y_test = train[FEATURES], train[TARGET], test[FEATURES], test[TARGET]
"""
print(X_train.isnull().sum())
print("----------")
print(X_test.isnull().sum())
"""
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
pred = model.predict(X_test_scaled)

from sklearn.metrics import accuracy_score, classification_report

print("LR Accuracy:")
print(f"accuracy score: {accuracy_score(y_test, pred)}")
print(f"classification report: {classification_report(y_test, pred)}")

print(matches1["target"].value_counts(normalize=True))

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split = 10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train_scaled, y_train)

rf_pred = rf.predict(X_test_scaled)

print("RF Accuracy:")
print(accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

import pandas as pd

importance = pd.DataFrame({"feature": FEATURES, "importance": rf.feature_importances_})
print(importance.sort_values("importance", ascending=False))


from xgboost import XGBClassifier

xgb = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.6,
    objective="multi:soft",
    num_class=3,
    random_state=42
)

xgb.fit(X_train_scaled, y_train)

xgb_pred = xgb.predict(X_test_scaled)

print("XGB Accuracy:")
print(accuracy_score(y_test, xgb_pred))
print(classification_report(y_test, xgb_pred))