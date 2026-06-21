from data_loader import load_data
results, rankings, world_cup, matches, matches1 = load_data()

#print(matches1.columns.tolist())
TOURNAMENT_WEIGHTS = {
    "Friendly": 1,

    "FIFA World Cup qualification": 2,
    "UEFA Euro qualification": 2,
    "African Cup of Nations qualification": 2,

    "AFC Asian Cup": 3,
    "African Cup of Nations": 3,
    "Gold Cup": 3,
    "Copa América": 3,
    "UEFA Euro": 3,

    "FIFA World Cup": 4
}

matches1["tournament_weight"] = (matches1["tournament"].map(TOURNAMENT_WEIGHTS).fillna(2))  #default = 2

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
    
    "home_last5_goal_diff",
    "away_last5_goal_diff",
    
    "tournament_weight",

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

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
"""
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
pred = model.predict(X_test_scaled)


print("LR Accuracy:")
print(f"accuracy score: {accuracy_score(y_test, pred)}")
print(f"classification report: {classification_report(y_test, pred)}")
"""

""" #i chose xgb since random forest was skipping draws, i analyzed confusion matrix because of it
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
print(confusion_matrix(y_test, rf_pred))

import pandas as pd

importance = pd.DataFrame({"feature": FEATURES, "importance": rf.feature_importances_})
print(importance.sort_values("importance", ascending=False))
"""
# now i need to try hyperparameter tuning to get best out of xgb
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV

param_grid = {
    "n_estimators": [200,400,600,800,1000],
    "max_depth": [3,4,5,6,8],
    "learning_rate": [0.01,0.03,0.05,0.1],
    "subsample": [0.7,0.8,0.9,1.0],
    "colsample_bytree": [0.7,0.8,0.9,1.0]
}

search = RandomizedSearchCV(
    estimator=XGBClassifier(objective="multi:softprob", num_class=3, random_state=42),
    param_distributions=param_grid,
    n_iter=10,
    cv=3,
    scoring="accuracy",
    n_jobs=-1,
    verbose=2,
    random_state=42
)

#search.fit(X_train_scaled, y_train)

#print(search.best_params_)
#print(search.best_score_)

# tuning results: {'subsample': 0.8, 'n_estimators': 200, 'max_depth': 4, 'learning_rate': 0.03, 'colsample_bytree': 0.7}
xgb = XGBClassifier(
    n_estimators=200,
    sub_sample=0.8,
    colsample_bytree=0.7,
    max_depth=4,
    learning_rate=0.03,
    objective="multi:softprob",
    num_class=3,
    random_state=42
)

xgb.fit(X_train_scaled, y_train)

xgb_pred = xgb.predict(X_test_scaled)

print("XGB Accuracy:")
print(accuracy_score(y_test, xgb_pred))
print(classification_report(y_test, xgb_pred))
print(confusion_matrix(y_test, xgb_pred))

#print(matches1["target"].value_counts(normalize=True))

import joblib
joblib.dump(xgb, "models/best_xgb_model.pkl")