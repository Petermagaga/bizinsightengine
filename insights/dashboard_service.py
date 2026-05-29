from insights.models import Insight

def get_dashboard_data(dataset):

    latest_insight = (
        Insight.objects
        .filter(dataset=dataset)
        .order_by("created_at")
        .first()
    )
    if latest_insight is None:
        return{
            "summary":None,
            "charts":[],
            "insights":[],
            "message":"No insights available yet"
        }

    return latest_insight.dashboard_data