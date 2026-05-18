from analytics.models import AnalysisResult


def build_dashboard(dataset):
    """
    Build chart-ready analytics data.
    """

    try:
        analysis = AnalysisResult.objects.get(
            dataset=dataset
        )

    except AnalysisResult.DoesNotExist:
        return {
            "error": "No analysis found"
        }

    summary = analysis.summary

    statistics = summary.get(
        "statistics", {}
    )

    mean_stats = statistics.get(
        "mean", {}
    )

    anomalies = summary.get(
        "anomalies", {}
    )

    # -----------------------
    # Top metrics chart
    # -----------------------
    sorted_metrics = sorted(
        mean_stats.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    top_metrics_chart = {
        "chart_type": "bar",
        "title": "Top Metrics",
        "labels": [
            key for key, _ in sorted_metrics
        ],
        "values": [
            value for _, value in sorted_metrics
        ]
    }

    # -----------------------
    # Anomaly chart
    # -----------------------
    anomaly_chart = {
        "chart_type": "pie",
        "title": "Anomalies",
        "labels": list(
            anomalies.keys()
        ),
        "values": list(
            anomalies.values()
        )
    }

    # -----------------------
    # Quality score
    # -----------------------
    quality_chart = {
        "chart_type": "gauge",
        "title": "Data Quality",
        "value": summary.get(
            "quality_score", 0
        )
    }

    return {
        "top_metrics": top_metrics_chart,
        "anomalies": anomaly_chart,
        "quality": quality_chart
    }