from celery import shared_task
from django.db import transaction
from django.utils import timezone

from data_ingestion.models import Dataset, DataRecord
from data_ingestion.utils.parse_excel import parse_excel


def clean_row(row):
    """
    Ensure JSON-safe values.
    """
    from datetime import datetime, date
    cleaned = {}

    for k, v in row.items():
        if isinstance(v, (datetime, date)):
            cleaned[k] = v.isoformat()
        elif v is None:
            cleaned[k] = None
        elif isinstance(v, (int, float, str, bool)):
            cleaned[k] = v
        else:
            cleaned[k] = str(v)  # fallback for unsupported types

    return cleaned


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def process_dataset_task(self, dataset_id):
    """
    Full pipeline:
    - Load dataset
    - Parse Excel
    - Clean data
    - Save records in batches
    - Update progress
    - Mark complete
    """

    dataset = Dataset.objects.get(id=dataset_id)

    try:
        # STEP 1: mark processing
        dataset.status = "processing"
        dataset.progress = 0
        dataset.started_at = timezone.now() if hasattr(dataset, "started_at") else None
        dataset.save(update_fields=["status"])

        # STEP 2: parse file
        parsed_data = list(parse_excel(dataset.file))

        total = len(parsed_data)
        if total == 0:
            dataset.status = "completed"
            dataset.progress = 100
            dataset.save(update_fields=["status", "progress"])
            return {"message": "Empty dataset"}

        batch_size = 500
        buffer = []

        # STEP 3: process rows
        for i, row in enumerate(parsed_data, start=1):
            clean_data = clean_row(row)

            buffer.append(DataRecord(
                dataset=dataset,
                data=clean_data
            ))

            # bulk insert (performance)
            if len(buffer) >= batch_size:
                DataRecord.objects.bulk_create(buffer)
                buffer = []

            # update progress every 100 rows
            if i % 100 == 0 or i == total:
                dataset.progress = int((i / total) * 100)
                dataset.save(update_fields=["progress"])

        # flush remaining
        if buffer:
            DataRecord.objects.bulk_create(buffer)

        # STEP 4: analytics hook (optional)
        # run your analytics here or trigger another task

        # STEP 5: mark complete
        dataset.status = "completed"
        dataset.progress = 100
        if hasattr(dataset, "completed_at"):
            dataset.completed_at = timezone.now()

        dataset.save(update_fields=["status", "progress"])

        return {
            "dataset_id": dataset.id,
            "rows_processed": total
        }

    except Exception as e:
        dataset.status = "failed"
        dataset.save(update_fields=["status"])
        raise e