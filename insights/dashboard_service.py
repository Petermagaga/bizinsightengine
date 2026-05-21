from insights.models import Insight
import pandas as pd
from datetime import datetime

def clean_metric_name(metric):
    return (
        metric
        .replace("_kgs", "")
        .replace("_pcs", "")
        .replace("_", " ")
        .title()
    )


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
            clean_metric_name(
            bi.get("top_metric","")),

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
                "label":clean_metric_name(
                    metric
                ),
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


    quality_score = (
        insight.bi_insights
        .get("quality_score", 0)
    )

    anomalies = (
        insight.bi_insights
        .get("anomalies_found", 0)
    )

    if quality_score >= 95 and anomalies < 20:
        business_health = "Excellent"

    elif quality_score >= 80:
        business_health = "Good"

    elif quality_score >= 60:
        business_health = "Warning"

    else:
        business_health = "Critical"

# -----------------------------
    # Dynamic Headline
    # -----------------------------

    if (
        trend_summary["increasing"]
        >
        trend_summary["decreasing"]
    ):

        if business_health == "Excellent":
            headline = (
                "Production increasing with healthy performance"
            )

        else:
            headline = (
                "Production improving across operations"
            )

    elif (
        trend_summary["decreasing"]
        >
        trend_summary["increasing"]
    ):

        headline = (
            "Production declining, attention required"
        )

    else:

        headline = (
            "Production stable across operations"
        )




    top_metric = kpis.get(
        "top_metric",
        "Unknown Metric"
    )

    anomalies_found = kpis.get(
        "anomalies_found",
        0
    )



    key_takeaway = (
        f"{top_metric} remains the top "
        f"performing product with "
        f"{anomalies_found} anomalies detected."
    )

    summary = {
        "headline": headline,
        "key_takeaway": key_takeaway
    }




    alerts = []

    # High anomaly warning
    if anomalies > 10:
        alerts.append({
            "type": "warning",
            "message":
            f"{anomalies} anomalies detected"
        })

    # Too many decreasing metrics
    if trend_summary["decreasing"] > (
        trend_summary["increasing"]
    ):
        alerts.append({
            "type": "risk",
            "message":
            "Production trend declining"
        })

    # Strong production health
    if business_health == "Excellent":
        alerts.append({
            "type": "success",
            "message":
            "Business performance healthy"
        })

    # Low stock risk
    for item in forecast_chart:
        metric = item["metric"]

        if (
            "balance_in_store" in metric
            and item["prediction"] < 50
        ):
            alerts.append({
                "type": "warning",
                "message":
                f"Low inventory risk: "
                f"{clean_metric_name(metric)}"
            })


    # -----------------------------
    # Recommendations Engine
    # -----------------------------




    recommendations = []

    priority_weights = {
        "low": 1,
        "medium": 2,
        "high": 3
    }
    # anomaly-based recommendation
    if anomalies_found > 10:
        priority="high"
        recommendations.append({
            "priority": "high",
            "severity":priority_weights[priority],
            "title": "Investigate anomalies",
            "message":
                (
                    f"{anomalies_found} anomalies "
                    "detected in production records."
                )
        })

    # inventory risk
    low_inventory_items = []

    for item in forecast_chart:
        metric = item["metric"].lower()

        if (
            "balance_in_store" in metric
            and item["prediction"] < 100
        ):
            low_inventory_items.append(
                item["label"]
            )

    if low_inventory_items:
        priority="medium"
        recommendations.append({
            "priority": "medium",
            "title": "Inventory replenishment",
            "severity":priority_weights[priority],
            "message":
                (
                    "Low inventory risk detected for: "
                    + ", ".join(low_inventory_items)
                )
        })

    # declining production trends
    decreasing_count = (
        trend_summary["decreasing"]
    )

    if decreasing_count > (
        trend_summary["increasing"]
    ):
        priority="high"
        recommendations.append({
            "priority": "high",
            "severity":priority_weights[priority],
            "severity":1,
            "title":
                "Production decline detected",
            "severity":priority_weights[priority],
            "message":
                (
                    "Several production "
                    "metrics are decreasing. "
                    "Review operations."
                )
        })

    # healthy business
    if business_health == "Excellent":
        priority="high"
        recommendations.append({
            "severity":priority_weights[priority],
            "title":
                "Maintain performance",

            "message":
                (
                    "Business performance "
                    "is healthy. Maintain "
                    "current operations."
                )
        })


    # -----------------------------
    # Predictive Alerts
    # -----------------------------
    predictive_alerts = []

    for item in forecast_chart:

        metric = item["metric"].lower()
        prediction = item["prediction"]
        trend = item["trend"]
        label = item["label"]

        # Inventory depletion risk
        if (
            "balance_in_store" in metric
            and prediction < 50
        ):

            predictive_alerts.append({
                "risk": "high",
                "title":
                    "Potential stock shortage",

                "message":
                    (
                        f"{label} inventory "
                        "may run low soon."
                    )
            })

        # Declining raw materials
        if (
            "raw_materials" in metric
            and trend == "decreasing"
            and prediction < 100
        ):

            predictive_alerts.append({
                "risk": "medium",
                "title":
                    "Raw material decline",

                "message":
                    (
                        f"{label} supply "
                        "is decreasing."
                    )
            })

        # Stock-out increase
        if (
            "stock_out" in metric
            and trend == "increasing"
        ):

            predictive_alerts.append({
                "risk": "high",
                "title":
                    "Stock-out risk increasing",

                "message":
                    (
                        f"{label} stock-outs "
                        "are trending upward."
                    )
            })

        # Production growth opportunity
        if (
            "final_product" in metric
            and trend == "increasing"
            and prediction > 1000
        ):

            predictive_alerts.append({
                "risk": "opportunity",
                "title":
                    "Production opportunity",

                "message":
                    (
                        f"{label} demand "
                        "appears strong."
                    )
            })


    # -----------------------------
    # Smart Decisions Engine
    # -----------------------------
    decisions = []

    for alert in predictive_alerts:

        title = alert["title"]
        message = alert["message"]
        risk = alert["risk"]

        # inventory shortage
        if (
            "stock shortage"
            in title.lower()
        ):

            decisions.append({
                "action":
                    "Increase inventory",

                "priority":
                    "high",

                "recommendation":
                    (
                        "Restock inventory "
                        "before next "
                        "production cycle."
                    )
            })

        # raw material decline
        elif (
            "raw material decline"
            in title.lower()
        ):

            decisions.append({
                "action":
                    "Procurement review",

                "priority":
                    "medium",

                "recommendation":
                    (
                        "Increase procurement "
                        "planning for declining "
                        "raw materials."
                    )
            })

        # stock-out increase
        elif (
            "stock-out risk"
            in title.lower()
        ):

            decisions.append({
                "action":
                    "Reduce stock-outs",

                "priority":
                    "high",

                "recommendation":
                    (
                        "Review production "
                        "and distribution "
                        "capacity."
                    )
            })

        # growth opportunity
        elif risk == "opportunity":

            decisions.append({
                "action":
                    "Scale production",

                "priority":
                    "medium",

                "recommendation":
                    (
                        "Increase production "
                        "capacity to meet "
                        "forecasted demand."
                    )
            })




    return {
        "kpis": kpis,
        "production_chart":
            production_chart,

        "forecast_chart":
            forecast_chart,

        "time_series":
        time_series,

        "trend_summary":
        trend_summary,

        "business_health":
        business_health,
        "summary":summary,

        "alerts":
        alerts,

        "recommendations":
        recommendations,

        "predictive_alerts":
        predictive_alerts,

        "decisions":decisions,
    }