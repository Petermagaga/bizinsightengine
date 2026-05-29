from insights.models import Insight

def get_dashboard_data(dataset):

    insight = (
        Insight.objects
        .filter(dataset=dataset)
        .latest("created_at")
    )

    return insight.dashboard_data