from data_ingestion.models import DataRecord

def compute_basic_statistics(dataset):
    records = DataRecord.objects.filter(dataset=dataset)

    if not records.exists():
        return {"message": "No data available"}

    numeric_fields = {}
    total_records = records.count()

    # collect numeric values
    for record in records:
        for key, value in record.data.items():
            if isinstance(value, (int, float)):
                numeric_fields.setdefault(key, []).append(value)

    # compute stats
    summary = {}

    for field, values in numeric_fields.items():
        total = sum(values)
        average = total / len(values) if values else 0

        summary[field] = {
            "total": total,
            "average": average
        }

    return {
        "total_records": total_records,
        "metrics": summary
    }