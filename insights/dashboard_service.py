from insights.models import Insight

def get_dashboard_data(dataset):

    latest_insight = (
        Insight.objects
        .filter(dataset=dataset)
        .order_by("created_at")
        .first()
    )
    if latest_insight is None:
        return {
            "summary": {
                "headline": "Processing...",
                "key_takeaway": "Insights are still being generated."
            },
            "kpis": {},
            "alerts": [],
            "recommendations": [],
            "decisions": {},
            "forecast_chart": [],
            "time_series": [],
            "business_health": "Unknown"
        }
    return latest_insight.dashboard_data