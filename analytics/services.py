from data_ingestion.models import DataRecord
from .models import AnalysisResult


def compute_basic_statistics(dataset):
    records = DataRecord.objects.filter(dataset=dataset)

    if not records.exists():
        return {"message": "No data available"}

    numeric_summary = {}

    all_rows = [record.data for record in records]

    for row in all_rows:
        for key, value in row.items():
            try:
                value = float(value)

                if key not in numeric_summary:
                    numeric_summary[key] = []

                numeric_summary[key].append(value)

            except (ValueError, TypeError):
                continue

    summary = {}

    for field, values in numeric_summary.items():
        if not values:
            continue

        summary[field] = {
            "total": sum(values),
            "average": round(sum(values) / len(values), 2),
            "max": max(values),
            "min": min(values),
            "trend": (
                "increasing"
                if values[-1] > values[0]
                else "decreasing"
                if values[-1] < values[0]
                else "stable"
            ),
        }

    analysis, _ = AnalysisResult.objects.update_or_create(
        dataset=dataset,
        defaults={"summary": summary}
    )

    return analysis.id