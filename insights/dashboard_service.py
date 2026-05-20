from insights.models import Insight


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

    for key, value in bi.items():

        if (
            isinstance(value, (int, float))
            and key.endswith("value")
        ):

            production_chart.append(
                {
                    "name": key,
                    "value": value
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

    return {
        "kpis": kpis,
        "production_chart":
            production_chart,

        "forecast_chart":
            forecast_chart
    }