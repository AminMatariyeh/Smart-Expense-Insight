import pandas as pd


def load_expenses(csv_file):
    df = pd.read_csv(csv_file)  
    print(df.head())  
    print (df.info())


    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    print (df.describe())

    print (df["Category"].value_counts())
    return df
