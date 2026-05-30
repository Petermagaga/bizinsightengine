import pandas as pd
from prophet import Prophet


def generate_forecast(records):

    df = pd.DataFrame(records)

    if "production_date" not in df.columns:
        return []

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    if len(numeric_cols) == 0:
        return []

    target_col = numeric_cols[0]

    forecast_df = pd.DataFrame({
        "ds": pd.to_datetime(
            df["production_date"]
        ),
        "y": df[target_col]
    })

    forecast_df = (
        forecast_df
        .dropna()
        .sort_values("ds")
    )

    if len(forecast_df) < 5:
        return []

    model = Prophet()

    model.fit(forecast_df)

    future = model.make_future_dataframe(
        periods=30
    )

    prediction = model.predict(
        future
    )

    results = []

    for _, row in prediction.tail(30).iterrows():

        results.append({
            "label": str(
                row["ds"].date()
            ),
            "prediction": round(
                row["yhat"],
                2
            )
        })

    return results