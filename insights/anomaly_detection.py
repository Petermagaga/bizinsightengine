import pandas as pd


def detect_anomalies(records):

    df = pd.DataFrame(records)

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    anomalies = []

    for col in numeric_cols:

        mean = df[col].mean()
        std = df[col].std()

        upper = mean + (2 * std)
        lower = mean - (2 * std)

        abnormal = df[
            (df[col] > upper) |
            (df[col] < lower)
        ]

        for _, row in abnormal.iterrows():

            anomalies.append({
                "column": col,
                "value": row[col],
                "reason": "Outside normal range"
            })

    return anomalies