from insights.models import Insight
import pandas as pd
from datetime import datetime
def get_dashboard_data(dataset):
    """
    Dashboard-ready analytics data.
    """

    try:
        insight = Insight.objects.filter(
            dataset=dataset
        ).latest("created_at")

    except Insight.DoesNotExist:
        return {
            "error": "No insights found"
        }

    bi = insight.bi_insights or {}
    predictions = (
        insight.predictions or {}
    )

    # -----------------------------
    # KPI Cards
    # -----------------------------
    kpis = {
        "quality_score":
            bi.get("quality_score"),

        "top_metric":
            bi.get("top_metric"),

        "top_value":
            bi.get("top_value"),

        "anomalies_found":
            bi.get(
                "anomalies_found",
                0
            ),

        "forecast_count":
            len(predictions)
    }

    # -----------------------------
    # Production Chart
    # -----------------------------

    production_chart = []

    for metric, data in (
        predictions.items()
    ):

        if (
            "final_product"
            in metric
        ):

            clean_name = (
                metric
                .replace(
                    "final_product_",
                    ""
                )
                .replace(
                    "_pcs",
                    ""
                )
                .replace(
                    "_kgs",
                    ""
                )
                .replace(
                    "_",
                    " "
                )
                .title()
            )

            production_chart.append(
                {
                    "name":
                        clean_name,

                    "value":
                        data.get(
                            "predicted_next",
                            0
                        )
                }
            )

    # -----------------------------
    # Forecast Chart
    # -----------------------------
    forecast_chart = []

    for metric, data in (
        predictions.items()
    ):

        forecast_chart.append(
            {
                "metric": metric,
                "prediction":
                    data.get(
                        "predicted_next",
                        0
                    ),
                "trend":
                    data.get(
                        "trend",
                        "stable"
                    )
            }
        )

    # -----------------------------
    # Time Series Chart
    # -----------------------------
    time_series = []

    try:

        records = (
            dataset.records
            .all()
            .values_list(
                "data",
                flat=True
            )
        )

        df = pd.DataFrame(records)

        if (
            "production_date"
            in df.columns
        ):

            production_column = (
                "final_product_fortified_maize_meal_2kg_pcs"
            )

            if (
                production_column
                in df.columns
            ):

                df[
                    production_column
                ] = pd.to_numeric(
                    df[
                        production_column
                    ],
                    errors="coerce"
                ).fillna(0)

                grouped = (
                    df.groupby(
                        "production_date"
                    )[
                        production_column
                    ]
                    .sum()
                    .reset_index()
                )


                daily_production = (
                    grouped.set_index(
                        "production_date"
                    )[
                        production_column
                    ].to_dict()
                )

                for date, total in sorted(
                    daily_production.items(),
                    key=lambda x: datetime.strptime(
                        str(x[0]),
                        "%d/%m/%Y"
                    )
                ):
                    
                    formatted_date=datetime.strptime(
                        str(date),
                        "%d/%m/%Y"
                    ).strftime("%Y-%m-%d")

                    time_series.append(
                        {
                            "date": formatted_date,
                            "production": round(total, 2)
                        }
                    )


    except Exception:
        time_series = []


    trend_summary = {
        "increasing": 0,
        "decreasing": 0,
        "stable": 0
    }

    for prediction in (
        insight.predictions.values()
    ):
        trend = prediction.get("trend")

        if trend in trend_summary:
            trend_summary[trend] += 1



    return {
        "kpis": kpis,
        "production_chart":
            production_chart,

        "forecast_chart":
            forecast_chart,

        "time_series":
        time_series,

        "trend_summary":
        trend_summary


    }