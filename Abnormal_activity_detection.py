import pandas as pd
from load_expenses import load_expenses
from sklearn.ensemble import IsolationForest

def detect_abnormalities(df, contamination=0.1):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    X = df[['Amount']]
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    df['abnormality'] = model.predict(X)

    return df[df['abnormality'] == -1]