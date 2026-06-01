import pandas as pd


def detect_anomalies(records):

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

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    anomalies = []

    for col in numeric_cols:

        values = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        mean = values.mean()
        std = values.std()

        # Skip columns with insufficient variation
        if pd.isna(std) or std == 0:
            continue

        upper = mean + (2 * std)
        lower = mean - (2 * std)

        abnormal_rows = df[
            (values > upper) |
            (values < lower)
        ]

        for _, row in abnormal_rows.iterrows():

            severity = "medium"

            value = row[col]

            if value > mean + (3 * std):
                severity = "high"

            elif value < mean - (3 * std):
                severity = "high"

            anomalies.append({
                "sheet_name": row.get(
                    "sheet_name"
                ),
                "column": col,
                "value": float(value),
                "mean": round(
                    float(mean),
                    2
                ),
                "upper_limit": round(
                    float(upper),
                    2
                ),
                "lower_limit": round(
                    float(lower),
                    2
                ),
                "severity": severity,
                "reason": (
                    "Outside expected range "
                    "(±2 standard deviations)"
                )
            })

    return anomalies