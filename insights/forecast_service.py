import pandas as pd
from prophet import Prophet


def generate_forecast(records):

    if not records:
        return []

    flattened_records = []

    for record in records:

        row_data = record.get("data", {}).copy()

        row_data["sheet_name"] = record.get(
            "sheet_name",
            "Unknown"
        )

        flattened_records.append(row_data)

    df = pd.DataFrame(flattened_records)

    if df.empty:
        return []

    forecasts = []

    for sheet_name in df["sheet_name"].unique():

        sheet_df = df[
            df["sheet_name"] == sheet_name
        ].copy()

        if "production_date" not in sheet_df.columns:
            continue

        sheet_df["production_date"] = pd.to_datetime(
            sheet_df["production_date"],
            errors="coerce"
        )

        sheet_df = sheet_df.dropna(
            subset=["production_date"]
        )

        if sheet_df.empty:
            continue

        numeric_cols = sheet_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        if not numeric_cols:
            continue

        # Prefer common business metrics
        preferred_cols = [
            "production",
            "output",
            "quantity",
            "qty",
            "stock",
            "inventory",
            "sales"
        ]

        target_col = None

        for col in preferred_cols:

            if col in numeric_cols:
                target_col = col
                break

        if target_col is None:
            target_col = numeric_cols[0]

        forecast_df = pd.DataFrame({
            "ds": sheet_df["production_date"],
            "y": pd.to_numeric(
                sheet_df[target_col],
                errors="coerce"
            )
        })

        forecast_df = (
            forecast_df
            .dropna()
            .sort_values("ds")
        )

        if len(forecast_df) < 5:
            continue

        try:

            model = Prophet()

            model.fit(forecast_df)

            future = model.make_future_dataframe(
                periods=30
            )

            prediction = model.predict(
                future
            )

            future_rows = prediction.tail(30)

            for _, row in future_rows.iterrows():

                forecasts.append({
                    "sheet_name": sheet_name,
                    "metric": target_col,
                    "label": str(
                        row["ds"].date()
                    ),
                    "prediction": round(
                        float(row["yhat"]),
                        2
                    ),
                    "lower_bound": round(
                        float(row["yhat_lower"]),
                        2
                    ),
                    "upper_bound": round(
                        float(row["yhat_upper"]),
                        2
                    ),
                    "trend": (
                        "up"
                        if row["yhat"] >
                        forecast_df["y"].mean()
                        else "down"
                    )
                })

        except Exception as e:

            print(
                f"Forecast failed for "
                f"{sheet_name}: {e}"
            )

            continue

    return forecasts