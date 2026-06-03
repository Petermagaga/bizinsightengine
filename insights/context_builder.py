def build_chat_context(
    dataset
):

    records = [
        {
            "sheet_name": r.sheet_name,
            "data": r.data
        }
        for r in dataset.records.all()[:20]
    ]

    total_records = (
        dataset.records.count()
    )

    columns = []

    if records:

        columns = list(
            records[0]["data"].keys()
        )

    latest_insight = (
        dataset.insights
        .order_by("-created_at")
        .first()
    )

    dashboard = {}

    if latest_insight:

        dashboard = (
            latest_insight.dashboard_data
        )

    return {
        "total_records": total_records,
        "columns": columns,
        "sample_records": records,
        "dashboard": dashboard
    }